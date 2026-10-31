"""Telegram formatting: model text must never crash a reply with "Can't parse entities"."""
import asyncio
import os
import types
from html.parser import HTMLParser

import pytest

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123:test")
os.environ.setdefault("GROQ_API_KEY", "test-key")

import src.telegram_bot as tb  # noqa: E402  (installs the safety net on import)

TRICKY = {
    "title": "Golden_Hour *Glow* [v2] `raw`",
    "style": "warm_cinematic <film> & grain",
    "prompt": "Using the reference photo, *keep* face_identical, \"Festival - 40% OFF\" `code` [link](x) <tag> & more",
    "negative_prompt": "blurry, extra_fingers, *watermark*",
    "aspect_ratio": "4:5",
    "keywords": ["beach_sunset", "*bold*", "<b>"],
}


class _TagChecker(HTMLParser):
    ALLOWED = {"b", "i", "code", "u", "s", "pre"}

    def __init__(self):
        super().__init__()
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in self.ALLOWED:
            self.errors.append(f"unexpected tag <{tag}>")
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag:
            self.errors.append(f"unbalanced </{tag}>")


def _render(variation, category="women_transform", monkeypatch=None):
    sent = []

    async def reply_text(text, **kwargs):
        sent.append((text, kwargs))

    message = types.SimpleNamespace(reply_text=reply_text)
    update = types.SimpleNamespace(message=message, callback_query=None,
                                   effective_chat=types.SimpleNamespace(id=1))
    context = types.SimpleNamespace(user_data={})
    handler = tb.TelegramBotHandler.__new__(tb.TelegramBotHandler)
    result = {"status": "success", "variations": [variation], "meta": {"emoji": "💕"}}
    asyncio.run(handler._handle_universal_prompts_response(update, context, result, category))
    return sent


@pytest.fixture(autouse=True)
def _no_history_writes(monkeypatch):
    import src.database.user_db as user_db
    monkeypatch.setattr(user_db, "save_history", lambda **kw: None, raising=False)


def test_variation_with_markdown_characters_renders_as_valid_html():
    sent = _render(TRICKY)
    html_messages = [t for t, kw in sent if kw.get("parse_mode") == "HTML"]
    assert len(html_messages) == 3  # header + one variation + next-steps summary
    for text in html_messages:
        checker = _TagChecker()
        checker.feed(text)
        assert not checker.errors and not checker.stack, (checker.errors, text)
    body = html_messages[1]
    assert "&lt;tag&gt;" in body and "&amp;" in body          # model text escaped
    assert "face_identical" in body and "*keep*" in body       # no Markdown escapes left behind
    assert "Markdown" not in [kw.get("parse_mode") for _, kw in sent]


def test_full_prompt_is_not_cut_at_500_characters():
    long_prompt = "Using the reference photo, " + "golden light on the sand, " * 40
    sent = _render({**TRICKY, "prompt": long_prompt})
    assert "golden light on the sand, " * 30 in sent[1][0]


def test_safety_net_resends_rejected_markdown_as_plain_text():
    from telegram import Message
    from telegram.error import BadRequest

    calls = []

    async def fake_original(self, text, **kwargs):
        calls.append((text, kwargs.get("parse_mode")))
        if kwargs.get("parse_mode"):
            raise BadRequest("Can't parse entities: can't find end of the entity starting at byte offset 116")
        return "sent"

    original = Message.reply_text
    try:
        # wrap a fake "original" exactly like the installed safety net does
        Message.reply_text = fake_original
        tb._install_parse_safety_net()
        result = asyncio.run(Message.reply_text(object(), "*Golden\\_Hour* `x`", parse_mode="Markdown"))
    finally:
        Message.reply_text = original
    assert result == "sent"
    assert calls[0][1] == "Markdown" and calls[1][1] is None
    assert calls[1][0] == "Golden_Hour x"


def test_safety_net_does_not_swallow_other_errors():
    from telegram import Message
    from telegram.error import BadRequest

    async def fake_original(self, text, **kwargs):
        raise BadRequest("Message is too long")

    original = Message.reply_text
    try:
        Message.reply_text = fake_original
        tb._install_parse_safety_net()
        with pytest.raises(BadRequest):
            asyncio.run(Message.reply_text(object(), "x", parse_mode="Markdown"))
    finally:
        Message.reply_text = original
