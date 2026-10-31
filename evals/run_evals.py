"""Run the golden eval set against the real Groq API (agentic report B1).

Usage (from telegram-insta-bot/):
    ./venv/Scripts/python.exe evals/run_evals.py                 # all cases
    ./venv/Scripts/python.exe evals/run_evals.py --only gen-     # cases whose id starts with "gen-"
    ./venv/Scripts/python.exe evals/run_evals.py --delay 20      # seconds between cases

Costs real tokens (~2-3K per case). The default delay keeps a full run under an 8,000 tokens/min
limit (about 6-8 minutes). Each run uses a throwaway SQLite DB, so cached answers never count as
passes and the real prompt log is untouched. Results go to evals/results/<timestamp>.json;
the exit code is 1 when the pass rate is below the threshold in golden_cases.json.
"""
import argparse
import asyncio
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
os.environ["SQLITE_DB_PATH"] = os.path.join(tempfile.mkdtemp(prefix="evals_"), "eval.db")
os.environ.setdefault("USER_TOKENS_PER_MIN", "0")  # never throttle the eval itself


# ── tiny path + check language ───────────────────────────────────────────────

def resolve(data, path):
    """'a.b[*].c' -> list of values ([*] fans out over list items)."""
    values = [data]
    for part in re.findall(r"[^.\[\]]+|\[\*\]", path):
        nxt = []
        for v in values:
            if part == "[*]":
                nxt.extend(v if isinstance(v, list) else [])
            elif isinstance(v, dict):
                if part in v:
                    nxt.append(v[part])
        values = nxt
    return values


def _words(v):
    return len(str(v).split())


def _int_between(v, lo_hi):
    try:
        return lo_hi[0] <= int(v) <= lo_hi[1] and float(v) == int(v)
    except (TypeError, ValueError):
        return False


OPS = {
    "equals": lambda vals, x: bool(vals) and vals[0] == x,
    "contains": lambda vals, x: bool(vals) and x.lower() in str(vals[0]).lower(),
    "not_contains": lambda vals, x: bool(vals) and x.lower() not in str(vals[0]).lower(),
    "contains_any": lambda vals, xs: bool(vals) and any(x.lower() in str(vals[0]).lower() for x in xs),
    "min_words": lambda vals, n: bool(vals) and _words(vals[0]) >= n,
    "max_words": lambda vals, n: bool(vals) and _words(vals[0]) <= n,
    "len_eq": lambda vals, n: bool(vals) and isinstance(vals[0], list) and len(vals[0]) == n,
    "len_ge": lambda vals, n: bool(vals) and isinstance(vals[0], (list, dict)) and len(vals[0]) >= n,
    "int_between": lambda vals, r: bool(vals) and _int_between(vals[0], r),
    "keys_start_with": lambda vals, p: bool(vals) and isinstance(vals[0], dict) and bool(vals[0])
    and all(str(k).startswith(p) for k in vals[0]),
    "each_contains": lambda vals, x: bool(vals) and all(x.lower() in str(v).lower() for v in vals),
    "each_not_contains": lambda vals, x: bool(vals) and all(x.lower() not in str(v).lower() for v in vals),
    "each_contains_any": lambda vals, xs: bool(vals) and all(any(x.lower() in str(v).lower() for x in xs) for v in vals),
    "each_in": lambda vals, xs: bool(vals) and all(str(v).strip() in xs for v in vals),
    "each_min_words": lambda vals, n: bool(vals) and all(_words(v) >= n for v in vals),
    "each_max_chars": lambda vals, n: bool(vals) and all(len(str(v)) <= n for v in vals),
    "each_regex": lambda vals, rx: bool(vals) and all(re.search(rx, str(v)) for v in vals),
    "each_int_between": lambda vals, r: bool(vals) and all(_int_between(v, r) for v in vals),
}


async def run_case(case, bot, orchestrator):
    kind, inp = case["kind"], case["input"]
    if kind == "orchestrator":
        return await orchestrator.execute(dict(inp))
    if kind == "chat":
        reply = await asyncio.to_thread(bot.chat_response, inp["message"], profile=inp.get("profile") or {})
        return {"reply": reply}
    if kind == "classify":
        commands = ["/generate", "/categories", "/search", "/content", "/inspire", "/trends", "/viral",
                    "/hashtags", "/engagement", "/monetize", "/analytics", "/report", "/stats", "/help"]
        return await asyncio.to_thread(bot.classify_intent, user_message=inp["message"], available_commands=commands)
    raise ValueError(f"unknown kind {kind}")


async def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", default="", help="run cases whose id starts with this prefix")
    parser.add_argument("--delay", type=float, default=15.0, help="seconds to wait between cases")
    parser.add_argument("--cases", default=str(HERE / "golden_cases.json"))
    args = parser.parse_args()

    from src.main import InstagramGrowthBot
    from src.agents.orchestrator import ContentOrchestratorAgent
    from src.observability import start_request

    spec = json.loads(Path(args.cases).read_text(encoding="utf-8"))
    cases = [c for c in spec["cases"] if c["id"].startswith(args.only)]
    bot = InstagramGrowthBot()
    orchestrator = ContentOrchestratorAgent(groq_bot=bot)
    print(f"Running {len(cases)} eval case(s) on model {bot.model}"
          f"{' (validator on)' if os.getenv('GENERATION_VALIDATE') == '1' else ''}\n")

    results = []
    for i, case in enumerate(cases):
        if i:
            await asyncio.sleep(args.delay)
        start_request(chat_id=case["input"].get("chat_id"), request_id=f"eval-{case['id']}")
        t0 = time.time()
        try:
            output = await run_case(case, bot, orchestrator)
            error = None
        except Exception as e:  # a crash is a failed case, not a crashed run
            output, error = {}, f"{type(e).__name__}: {e}"
        checks = []
        for chk in case["checks"]:
            vals = resolve(output, chk["path"])
            try:
                ok = bool(OPS[chk["op"]](vals, chk["value"]))
            except Exception:
                ok = False
            checks.append({**chk, "passed": ok, "actual": str(vals[:3])[:200]})
        passed = error is None and all(c["passed"] for c in checks)
        results.append({"id": case["id"], "passed": passed, "seconds": round(time.time() - t0, 1),
                        "error": error, "checks": checks,
                        "output_preview": json.dumps(output, ensure_ascii=False, default=str)[:600]})
        failed = [f"{c['path']} {c['op']}" for c in checks if not c["passed"]]
        print(f"{'PASS' if passed else 'FAIL'}  {case['id']:<24} {results[-1]['seconds']:>5}s"
              + (f"  error={error}" if error else "") + (f"  failed: {failed}" if failed else ""))

    n_pass = sum(r["passed"] for r in results)
    rate = n_pass / len(results) if results else 0.0
    threshold = spec.get("pass_threshold", 0.85)
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    out_file.write_text(json.dumps({"model": bot.model, "pass_rate": rate, "threshold": threshold,
                                    "validator": os.getenv("GENERATION_VALIDATE", "0"),
                                    "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{n_pass}/{len(results)} passed ({rate:.0%}, threshold {threshold:.0%}). Details: {out_file}")
    return 0 if rate >= threshold else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
