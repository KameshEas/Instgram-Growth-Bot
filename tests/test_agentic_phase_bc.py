"""Phases B and C of the agentic upgrade: persistence, validator retry, eval runner, chat agent, contracts."""
import asyncio
import importlib.util
import json
import os
import types
from pathlib import Path

import pytest

os.environ.setdefault("GROQ_API_KEY", "test-key")
ROOT = Path(__file__).resolve().parent.parent


# ── shared fixtures ──────────────────────────────────────────────────────────

def _response(content="", tool_calls=None, tokens=100):
    msg = types.SimpleNamespace(content=content, tool_calls=tool_calls)
    usage = types.SimpleNamespace(prompt_tokens=tokens - 20, completion_tokens=20, total_tokens=tokens)
    return types.SimpleNamespace(choices=[types.SimpleNamespace(message=msg)], usage=usage)


class ScriptedClient:
    """Returns the scripted responses in order and records every request."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []
        self.chat = types.SimpleNamespace(completions=types.SimpleNamespace(create=self._create))

    def _create(self, **kw):
        self.calls.append(json.loads(json.dumps(kw, default=str)))
        return self.responses.pop(0)


@pytest.fixture
def bot(monkeypatch, tmp_path):
    import src.main as main
    import src.database.prompt_log as plog
    import src.database.user_db as udb
    import src.services.token_budget as tb
    from src.services.groq_retry_handler import GroqRetryHandler, GroqRetryConfig

    monkeypatch.setattr(plog, "DB_PATH", str(tmp_path / "log.db"))
    monkeypatch.setattr(udb, "DB_PATH", str(tmp_path / "users.db"))
    plog.init_prompt_log_db()
    monkeypatch.setattr(main, "PROMPT_LOG_ENABLED", True)
    monkeypatch.setattr(main, "METRICS_ENABLED", False)
    monkeypatch.setattr(tb, "_budget", tb.TokenBudget(0))
    b = main.InstagramGrowthBot.__new__(main.InstagramGrowthBot)
    b.model = "m"
    b.retry_handler = GroqRetryHandler(GroqRetryConfig(max_retries=0))
    return b


# ── B3: conversation state persistence ───────────────────────────────────────

def test_conversation_state_round_trip(bot):
    from src.database.user_db import get_conversation_state, save_conversation_state

    assert get_conversation_state(1) == {"chat_history": [], "pending_clarification": None}
    turns = [{"role": "user", "content": f"q{i}"} for i in range(10)]
    save_conversation_state(1, chat_history=turns, pending_clarification={"question": "Which colors?"})
    state = get_conversation_state(1)
    assert len(state["chat_history"]) == 6 and state["chat_history"][-1]["content"] == "q9"
    assert state["pending_clarification"]["question"] == "Which colors?"
    save_conversation_state(1, pending_clarification=None)       # clearing keeps history
    state = get_conversation_state(1)
    assert state["pending_clarification"] is None and len(state["chat_history"]) == 6


def test_handler_restores_state_after_restart(bot, monkeypatch):
    import src.telegram_bot as tbot
    from src.database.user_db import save_conversation_state

    monkeypatch.setenv("PERSIST_CHAT_STATE", "1")
    save_conversation_state(77, chat_history=[{"role": "user", "content": "hello"}],
                            pending_clarification={"question": "Which style?", "input": {}})
    handler = tbot.TelegramBotHandler.__new__(tbot.TelegramBotHandler)
    context = types.SimpleNamespace(user_data={})                # fresh process: nothing in memory
    handler._restore_state(context, 77)
    assert context.user_data["chat_history"][0]["content"] == "hello"
    assert context.user_data["pending_clarification"]["question"] == "Which style?"


def test_state_not_persisted_when_flag_off(bot, monkeypatch):
    import src.telegram_bot as tbot
    from src.database.user_db import get_conversation_state

    monkeypatch.delenv("PERSIST_CHAT_STATE", raising=False)
    handler = tbot.TelegramBotHandler.__new__(tbot.TelegramBotHandler)
    handler._persist_state(types.SimpleNamespace(user_data={"chat_history": [{"role": "user", "content": "x"}]}), 5)
    assert get_conversation_state(5)["chat_history"] == []


# ── B2: validator + one bounded retry ────────────────────────────────────────

GOOD = {"title": "T", "style": "S", "negative_prompt": "blurry", "aspect_ratio": "4:5", "keywords": ["k"]}
PROMPT_OK = ("Vertical festive poster with the headline \"Festival Sale\" in bold type, warm diya glow, #FF6B00 "
             "accents, centered layout, soft bokeh lights, crisp print detail, high contrast, clean margins, "
             "warm candlelight, rich colors")


def test_validator_rules():
    from src.services.variation_validator import required_literals, validate_variations

    literals = required_literals('poster "Festival Sale" in #FF6B00')
    assert literals == ["Festival Sale", "#FF6B00"]
    good = [{**GOOD, "prompt": PROMPT_OK} for _ in range(3)]
    assert validate_variations(good, 3, "design_posters", False, literals) == []
    bad = [{**GOOD, "prompt": "short prompt", "aspect_ratio": "7:3"}]
    problems = validate_variations(bad, 3, "design_posters", False, literals)
    text = " ".join(problems)
    assert "exactly 3" in text and "aspect_ratio" in text and "too short" in text and "Festival Sale" in text
    transform = [{**GOOD, "prompt": PROMPT_OK}]
    assert any("reference photo" in p for p in validate_variations(transform, 1, "women_transform", False))


def test_generation_retries_once_with_feedback(bot, monkeypatch):
    monkeypatch.setenv("GENERATION_VALIDATE", "1")
    first = {"variations": [{**GOOD, "prompt": "too short"}]}
    second = {"variations": [{**GOOD, "prompt": PROMPT_OK} for _ in range(3)]}
    bot.client = ScriptedClient([_response(json.dumps(first)), _response(json.dumps(second))])
    result = bot.generate_universal_prompts(category="design_posters",
                                            user_idea='poster "Festival Sale" in #FF6B00', count=3)
    assert result["status"] == "success" and len(result["variations"]) == 3
    assert len(bot.client.calls) == 2
    retry_user_msg = bot.client.calls[1]["messages"][-1]["content"]
    assert "did not meet these requirements" in retry_user_msg and "exactly 3" in retry_user_msg


def test_contract_violation_triggers_one_retry(bot, monkeypatch):
    monkeypatch.setenv("GENERATION_VALIDATE", "1")
    incomplete = {"engagement_targets": {"daily_follows": 10, "daily_likes": 50, "daily_comments": 10},
                  "timing_recommendations": None}
    complete = {**incomplete, "timing_recommendations": {"peak_hours": ["7-9 PM IST"], "best_days": ["Sunday"]}}
    bot.client = ScriptedClient([_response(json.dumps(incomplete)), _response(json.dumps(complete))])
    result = bot.engagement_strategy(account_size="micro")
    assert result["timing_recommendations"]["peak_hours"] == ["7-9 PM IST"]
    assert len(bot.client.calls) == 2
    assert "timing_recommendations" in bot.client.calls[1]["messages"][-1]["content"]


def test_transform_categories_have_identity_guidance():
    from src.prompts.dynamic_context_builder import DynamicContextBuilder

    for category in ("women_transform", "men_transform", "couples_transform"):
        guidance = DynamicContextBuilder.build_category_guidance(category)
        assert "Using the reference photo" in guidance and "never morph" in guidance


def test_no_retry_when_flag_off_or_valid(bot, monkeypatch):
    monkeypatch.delenv("GENERATION_VALIDATE", raising=False)
    bot.client = ScriptedClient([_response(json.dumps({"variations": [{**GOOD, "prompt": "short"}]}))])
    bot.generate_universal_prompts(category="design_posters", user_idea="poster", count=3)
    assert len(bot.client.calls) == 1


# ── B1: eval runner check language (no network) ──────────────────────────────

def _load_runner():
    spec = importlib.util.spec_from_file_location("run_evals", ROOT / "evals" / "run_evals.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_eval_runner_paths_and_ops():
    runner = _load_runner()
    data = {"variations": [{"prompt": "Using the reference photo, beach"}, {"prompt": "reference photo, sand"}],
            "report": {"metrics": {"estimated_reach": 10}}, "status": "success"}
    assert runner.resolve(data, "variations[*].prompt") == ["Using the reference photo, beach", "reference photo, sand"]
    assert runner.OPS["each_contains"](runner.resolve(data, "variations[*].prompt"), "reference photo")
    assert not runner.OPS["each_contains"](runner.resolve(data, "variations[*].prompt"), "beach")
    assert runner.OPS["keys_start_with"](runner.resolve(data, "report.metrics"), "estimated_")
    assert runner.OPS["each_int_between"]([5, 50], [0, 100]) and not runner.OPS["each_int_between"](["x"], [0, 1])
    assert not runner.OPS["equals"]([], "success")               # missing path never passes


def test_golden_cases_are_well_formed():
    runner = _load_runner()
    spec = json.loads((ROOT / "evals" / "golden_cases.json").read_text(encoding="utf-8"))
    ids = [c["id"] for c in spec["cases"]]
    assert len(ids) == len(set(ids)) >= 15
    for case in spec["cases"]:
        assert case["kind"] in ("orchestrator", "chat", "classify")
        for chk in case["checks"]:
            assert chk["op"] in runner.OPS, (case["id"], chk["op"])


# ── C1: chat coach agent ─────────────────────────────────────────────────────

def _tool_call(name, args="{}", call_id="call_1"):
    payload = {"id": call_id, "type": "function", "function": {"name": name, "arguments": args}}
    return types.SimpleNamespace(model_dump=lambda: payload)


def test_agent_calls_tool_then_answers(bot):
    from src.agents.chat_agent import ChatCoachAgent

    bot.client = ScriptedClient([
        _response(tool_calls=[_tool_call("get_creator_profile")]),
        _response(content="Post 3 Reels a week about street food."),
    ])
    agent = ChatCoachAgent(bot, profile_lookup=lambda cid: {"niche": "street food"})
    answer = agent.respond("What should I post?", profile={"chat_id": 11})
    assert answer.startswith("Post 3 Reels")
    second = bot.client.calls[1]["messages"]
    tool_msg = [m for m in second if m["role"] == "tool"][0]
    assert tool_msg["tool_call_id"] == "call_1"
    assert tool_msg["content"].startswith("<tool_result>") and "street food" in tool_msg["content"]
    assert bot.client.calls[0]["extra_body"]["tool_choice"] == "auto"


def test_agent_step_budget_forces_final_answer(bot):
    from src.agents.chat_agent import ChatCoachAgent, MAX_STEPS

    bot.client = ScriptedClient(
        [_response(tool_calls=[_tool_call("get_creator_profile", call_id=f"c{i}")]) for i in range(MAX_STEPS - 1)]
        + [_response(content="Here is my answer.", tool_calls=[_tool_call("get_creator_profile", call_id="late")])]
    )
    answer = ChatCoachAgent(bot).respond("loop forever", profile={"chat_id": 12})
    assert answer == "Here is my answer."
    assert len(bot.client.calls) == MAX_STEPS
    assert bot.client.calls[-1]["extra_body"]["tool_choice"] == "none"


def test_agent_handles_unknown_tool_and_bad_args(bot):
    from src.agents.chat_agent import ChatCoachAgent

    bot.client = ScriptedClient([
        _response(tool_calls=[_tool_call("delete_account"), _tool_call("get_recent_generations", "{not json", "c2")]),
        _response(content="Sorry, I can only read your data."),
    ])
    answer = ChatCoachAgent(bot).respond("delete my account", profile={"chat_id": 13})
    assert "only read" in answer
    tool_contents = [m["content"] for m in bot.client.calls[1]["messages"] if m["role"] == "tool"]
    assert "unknown tool" in tool_contents[0] and "not valid JSON" in tool_contents[1]


def test_tool_output_is_bounded():
    from src.agents.chat_agent import _bounded, MAX_TOOL_OUTPUT_CHARS

    out = _bounded({"x": "y" * 10_000})
    assert len(out) < MAX_TOOL_OUTPUT_CHARS + 60 and "truncated" in out


def test_plain_text_strips_markdown():
    from src.agents.chat_agent import plain_text

    assert plain_text("1. **Festive Bundle**\n## Tips\n* one\n__two__") == "1. Festive Bundle\nTips\n- one\ntwo"


def test_agent_flag_default_off(monkeypatch):
    from src.agents.chat_agent import chat_agent_enabled

    monkeypatch.delenv("CHAT_AGENT", raising=False)
    assert not chat_agent_enabled()


# ── C2: contracts + style hints ──────────────────────────────────────────────

def test_contract_errors_flag_missing_keys():
    from src.contracts import contract_errors

    assert contract_errors("analyze_trends", {"trending_topics": [{"topic": "x", "viral_potential": 70}]}) == []
    errs = contract_errors("analyze_trends", {"trending_hashtags": []})
    assert errs and "trending_topics" in errs[0]
    assert contract_errors("engagement_strategy", {"engagement_targets": {"daily_follows": 5, "daily_likes": 5,
                                                   "daily_comments": 5}, "timing_recommendations": {}}) == []
    assert contract_errors("unknown_command", {}) is None


def test_prompt_shapes_satisfy_contracts():
    """The JSON shape each prompt shows must pass its own contract (prompt <-> contract drift check)."""
    import src.main as main
    from src.contracts import contract_errors
    from tests.test_prompt_contracts import _shape

    bot = main.InstagramGrowthBot.__new__(main.InstagramGrowthBot)
    bot.model = "m"
    captured = {}
    bot._call_groq_with_fallback = lambda **kw: captured.update(kw) or {}
    cases = {
        "generate_content": dict(topic="t", style="s"), "analyze_trends": dict(niche="n"),
        "engagement_strategy": dict(account_size="micro"), "monetization_ideas": dict(niche="n", follower_count=1),
        "caption_generator": dict(post_description="p"), "hashtag_pack": dict(topic="t"),
        "bio_optimizer": dict(current_bio="b"), "classify_intent": dict(user_message="m", available_commands=["/help"]),
    }
    for method, kwargs in cases.items():
        getattr(bot, method)(**kwargs)
        errs = contract_errors(captured["command"], _shape(captured["prompt"]))
        assert errs == [], (method, errs)


def test_style_hints_from_favorites(bot, monkeypatch):
    from src.agents.content_generator import ContentGeneratorAgent
    from src.database.user_db import save_favorite

    monkeypatch.setenv("STYLE_HINTS", "1")
    save_favorite(chat_id=21, category="design_posters", prompt="p", title="Golden Diya Sale",
                  style="festive cinematic poster")
    agent = ContentGeneratorAgent.__new__(ContentGeneratorAgent)
    agent.logger = types.SimpleNamespace(warning=lambda *a, **k: None)
    hints = agent._style_hints(21, "design_posters")
    assert "Golden Diya Sale" in hints and "festive cinematic poster" in hints and "optional" in hints
    assert agent._style_hints(21, "logo_create") == ""
    monkeypatch.delenv("STYLE_HINTS")
    assert agent._style_hints(21, "design_posters") == ""
