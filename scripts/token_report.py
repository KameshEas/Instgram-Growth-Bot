"""Token usage report from the prompt log (agentic report A2).

Usage:
    python scripts/token_report.py                 # last 24 hours
    python scripts/token_report.py --hours 168     # last 7 days
    python scripts/token_report.py --request <id>  # every LLM call for one user request

Reads data/users.db (or SQLITE_DB_PATH). Rows written before token logging existed have no
token counts and are reported as "untracked".
"""
import argparse
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent.parent / "data" / "users.db"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--hours", type=float, default=24)
    parser.add_argument("--request", help="show every call for one request_id")
    parser.add_argument("--db", default=os.getenv("SQLITE_DB_PATH", str(DEFAULT_DB)))
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cols = {r[1] for r in conn.execute("PRAGMA table_info(prompt_response_logs)")}
    if "total_tokens" not in cols:
        print("No token columns yet: start the bot once so the prompt log migrates.")
        return

    if args.request:
        rows = conn.execute(
            "SELECT created_at, command, model, success, latency_ms, prompt_tokens, completion_tokens, "
            "total_tokens, error_msg FROM prompt_response_logs WHERE request_id = ? ORDER BY id",
            (args.request,),
        ).fetchall()
        print(f"Request {args.request}: {len(rows)} LLM call(s)")
        for r in rows:
            status = "ok" if r["success"] else f"FAILED ({(r['error_msg'] or '')[:80]})"
            print(f"  {r['created_at']}  {r['command']:<28} {r['model'] or '':<22} "
                  f"{r['latency_ms'] or 0:>6} ms  tokens={r['total_tokens'] or '-'}  {status}")
        return

    since = (datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=args.hours)).isoformat()
    rows = conn.execute(
        """
        SELECT command,
               COUNT(*)                                   AS calls,
               SUM(success)                               AS ok,
               SUM(COALESCE(total_tokens, 0))             AS tokens,
               SUM(CASE WHEN total_tokens IS NULL THEN 1 ELSE 0 END) AS untracked,
               AVG(latency_ms)                            AS avg_ms
        FROM prompt_response_logs
        WHERE created_at >= ?
        GROUP BY command
        ORDER BY tokens DESC
        """,
        (since,),
    ).fetchall()
    total_tokens = sum(r["tokens"] for r in rows)
    print(f"LLM usage, last {args.hours:g} h ({args.db})")
    print(f"{'command':<30}{'calls':>7}{'ok':>6}{'tokens':>10}{'avg tok':>9}{'avg ms':>9}{'untracked':>11}")
    for r in rows:
        tracked = r["calls"] - r["untracked"]
        avg_tok = int(r["tokens"] / tracked) if tracked else 0
        print(f"{r['command']:<30}{r['calls']:>7}{r['ok'] or 0:>6}{r['tokens']:>10}{avg_tok:>9}"
              f"{int(r['avg_ms'] or 0):>9}{r['untracked']:>11}")
    print(f"{'TOTAL':<30}{sum(r['calls'] for r in rows):>7}{'':>6}{total_tokens:>10}")

    top = conn.execute(
        "SELECT chat_id, SUM(COALESCE(total_tokens,0)) AS tokens, COUNT(*) AS calls "
        "FROM prompt_response_logs WHERE created_at >= ? AND chat_id IS NOT NULL "
        "GROUP BY chat_id ORDER BY tokens DESC LIMIT 5",
        (since,),
    ).fetchall()
    if top:
        print("\nTop users by tokens:")
        for r in top:
            print(f"  chat {r['chat_id']}: {r['tokens']} tokens over {r['calls']} calls")


if __name__ == "__main__":
    main()
