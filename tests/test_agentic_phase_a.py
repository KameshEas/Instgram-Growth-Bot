"""Phase A of the agentic upgrade: fallback, tracing/tokens, budgets, bounded eval log, parallel scraping."""
import asyncio
import os
import sqlite3
import time
import types

import pytest

os.environ.setdefault("GROQ_API_KEY", "test-key")


# ── helpers ──────────────────────────────────────────────────────────────────

class FakeCompletions:
    """Scripted Groq client: per-model behaviour = "ok" | an exception message to raise."""

    def __init__(self, behaviour):
        self.behaviour = behaviour
        self.calls = []

    def create(self, **kw):
        self.calls.append(kw)
        b = self.behaviour.get(kw["model"], "ok")
        if b != "ok":
            raise Exception(b)
        msg = types.SimpleNamespace(content='{"answer": "ok"}')
        usage = types.SimpleNamespace(prompt_tokens=100, completion_tokens=20, total_tokens=120)
        return types.SimpleNamespace(choices=[types.SimpleNamespace(message=msg)], usage=usage)


@pytest.fixture
def bot(monkeypatch, tmp_path):
    import src.main as main
    import src.database.prompt_log as plog
    from src.services.groq_retry_handler import GroqRetryHandler, GroqRetryConfig
    import src.services.token_budget as tb

    monkeypatch.setattr(plog, "DB_PATH", str(tmp_path / "log.db"))
    plog.init_prompt_log_db()
    monkeypatch.setattr(main, "PROMPT_LOG_ENABLED", True)
    monkeypatch.setattr(main, "METRICS_ENABLED", False)
    monkeypatch.setattr(tb, "_budget", tb.TokenBudget(0))  # disabled unless a test enables it

    b = main.InstagramGrowthBot.__new__(main.InstagramGrowthBot)
    b.model = "primary-model"
    b.retry_handler = GroqRetryHandler(GroqRetryConfig(max_retries=0))
    b._db_path = str(tmp_path / "log.db")
    return b


def _rows(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn.execute("SELECT * FROM prompt_response_logs ORDER BY id").fetchall()


# ── A1: model fallback chain ─────────────────────────────────────────────────

def test_falls_back_when_primary_model_is_retired(bot, monkeypatch):
    monkeypatch.setenv("GROQ_MODEL_FALLBACKS", "backup-model")
    fake = FakeCompletions({"primary-model": "Error code: 404 - model_not_found: does not exist"})
    bot.client = types.SimpleNamespace(chat=types.SimpleNamespace(completions=fake))
    result = bot._call_groq_with_fallback(command="t", cache_key="", prompt="p", ttl_hours=None)
    assert result == {"answer": "ok"}
    assert [c["model"] for c in fake.calls] == ["primary-model", "backup-model"]
    assert _rows(bot._db_path)[-1]["model"] == "backup-model"


def test_no_fallback_for_request_errors(bot, monkeypatch):
    monkeypatch.setenv("GROQ_MODEL_FALLBACKS", "backup-model")
    fake = FakeCompletions({"primary-model": "Error code: 401 - invalid api key"})
    bot.client = types.SimpleNamespace(chat=types.SimpleNamespace(completions=fake))
    result = bot._call_groq_with_fallback(command="t", cache_key="", prompt="p", ttl_hours=None)
    assert "error" in result
    assert [c["model"] for c in fake.calls] == ["primary-model"]


def test_without_fallback_env_only_primary_is_tried(bot, monkeypatch):
    monkeypatch.delenv("GROQ_MODEL_FALLBACKS", raising=False)
    fake = FakeCompletions({"primary-model": "Error code: 404 - model_not_found"})
    bot.client = types.SimpleNamespace(chat=types.SimpleNamespace(completions=fake))
    assert "error" in bot._call_groq_with_fallback(command="t", cache_key="", prompt="p", ttl_hours=None)
    assert len(fake.calls) == 1


def test_client_errors_do_not_open_circuit_breaker():
    from src.services.groq_retry_handler import GroqRetryHandler, GroqRetryConfig, CircuitState

    handler = GroqRetryHandler(GroqRetryConfig(max_retries=0, circuit_failure_threshold=2))

    def bad_request():
        raise Exception("Error code: 404 - model_not_found")

    for _ in range(5):
        handler.call_with_retry(bad_request)
    assert handler.circuit_state == CircuitState.CLOSED


# ── A2: token accounting + request tracing ──────────────────────────────────

def test_tokens_and_request_id_are_logged(bot):
    from src.observability import start_request

    bot.client = types.SimpleNamespace(chat=types.SimpleNamespace(completions=FakeCompletions({})))
    rid = start_request(chat_id=42)
    bot._call_groq_with_fallback(command="first", cache_key="", prompt="p1", ttl_hours=None)
    bot._call_groq_with_fallback(command="second", cache_key="", prompt="p2", ttl_hours=None)
    rows = _rows(bot._db_path)
    assert [r["request_id"] for r in rows] == [rid, rid]
    assert all(r["chat_id"] == 42 for r in rows)               # chat comes from the request context
    assert rows[0]["total_tokens"] == 120 and rows[0]["prompt_tokens"] == 100


def test_request_context_survives_to_thread():
    from src.observability import start_request, current_request_id

    async def main():
        rid = start_request(chat_id=7)
        return rid, await asyncio.to_thread(current_request_id)

    rid, seen = asyncio.run(main())
    assert rid == seen


def test_migration_adds_columns_to_old_table(tmp_path, monkeypatch):
    import src.database.prompt_log as plog

    db = tmp_path / "old.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE prompt_response_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER, "
                 "command TEXT NOT NULL, prompt_hash TEXT NOT NULL, prompt_text TEXT NOT NULL, response_json TEXT, "
                 "success INTEGER NOT NULL DEFAULT 0, error_msg TEXT, latency_ms INTEGER, model TEXT, "
                 "created_at TEXT NOT NULL)")
    conn.commit(); conn.close()
    monkeypatch.setattr(plog, "DB_PATH", str(db))
    plog.init_prompt_log_db()
    cols = {r[1] for r in sqlite3.connect(db).execute("PRAGMA table_info(prompt_response_logs)")}
    assert {"prompt_tokens", "completion_tokens", "total_tokens", "request_id"} <= cols


# ── A3: per-user token budget ───────────────────────────────────────────────

def test_budget_blocks_then_recovers():
    from src.services.token_budget import TokenBudget

    now = [1000.0]
    budget = TokenBudget(1000, clock=lambda: now[0])
    assert budget.check("u")[0]
    budget.record("u", 1200)
    allowed, retry_after = budget.check("u")
    assert not allowed and 1 <= retry_after <= 61
    assert budget.check("someone-else")[0]                     # budgets are per user
    now[0] += 61
    assert budget.check("u")[0]


def test_budget_disabled_by_default(monkeypatch):
    from src.services.token_budget import TokenBudget

    monkeypatch.delenv("USER_TOKENS_PER_MIN", raising=False)
    budget = TokenBudget()
    budget.record("u", 10 ** 9)
    assert budget.check("u") == (True, 0)


def test_gateway_returns_friendly_error_when_over_budget(bot, monkeypatch):
    import src.services.token_budget as tb

    monkeypatch.setattr(tb, "_budget", tb.TokenBudget(100))
    fake = FakeCompletions({})
    bot.client = types.SimpleNamespace(chat=types.SimpleNamespace(completions=fake))
    first = bot._call_groq_with_fallback(command="t", cache_key="", prompt="p", chat_id=5, ttl_hours=None)
    second = bot._call_groq_with_fallback(command="t", cache_key="", prompt="p2", chat_id=5, ttl_hours=None)
    assert first == {"answer": "ok"}
    assert second.get("rate_limited") and "wait" in second["error"]
    assert len(fake.calls) == 1                                # the second call never reached Groq


# ── A4: bounded evaluation log ──────────────────────────────────────────────

def test_evaluation_log_is_bounded(monkeypatch, tmp_path):
    import src.services.agent_evaluation_integration as aei

    hook = aei.AgentEvaluationHook.__new__(aei.AgentEvaluationHook)
    hook.agent_name = "T"
    hook.evaluation_log = []
    hook.metrics_dir = tmp_path

    class FakeEval:
        overall_rating = 7

        def to_dict(self):
            return {"overall_rating": 7}

    async def fake_evaluate(**kw):
        return FakeEval()

    hook.evaluator = types.SimpleNamespace(evaluate=fake_evaluate)
    hook._generate_recommendations = lambda e: []
    monkeypatch.setattr(aei, "MAX_IN_MEMORY_EVALUATIONS", 50)

    async def run():
        for i in range(120):
            await hook.evaluate_execution({"category": "x"}, {"variations": [{"prompt": str(i)}]})

    asyncio.run(run())
    assert len(hook.evaluation_log) == 50


# ── A5: parallel scraping ───────────────────────────────────────────────────

def test_scrapers_run_in_parallel_and_tolerate_failures():
    from src.agents.trends_agent import TrendsAgent

    agent = TrendsAgent(groq_bot=None)

    async def slow_reddit():
        time.sleep(0.5)
        return ["r1"]

    async def slow_github():
        time.sleep(0.5)
        raise RuntimeError("github down")

    async def slow_news():
        time.sleep(0.5)
        return ["n1"]

    agent._fetch_reddit_trends = slow_reddit
    agent._fetch_github_trends = slow_github
    agent._fetch_news_topics = slow_news
    start = time.time()
    reddit, github, news = asyncio.run(agent._scrape_all())
    elapsed = time.time() - start
    assert (reddit, github, news) == (["r1"], [], ["n1"])
    assert elapsed < 1.2, f"scrapers ran sequentially ({elapsed:.2f}s)"
