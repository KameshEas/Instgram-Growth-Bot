"""SQLite-backed prompt logging and AI response cache.

Extends data/users.db with two tables:
  - prompt_response_logs : append-only audit of every AI call
  - ai_response_cache    : keyed fallback store with per-command TTL

Uses the same stdlib sqlite3 pattern as user_db.py — no new dependencies.
"""

import hashlib
import json
import logging
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# DB path mirrors user_db.py resolution
_DEFAULT_DB = str(Path(__file__).parent.parent.parent / "data" / "users.db")
DB_PATH: str = os.getenv("SQLITE_DB_PATH", _DEFAULT_DB)

# Default TTL (hours) per command — trends expire fastest, strategies last longest
COMMAND_TTL: Dict[str, int] = {
    "analyze_trends": 6,
    "generate_content": 24,
    "engagement_strategy": 48,
    "get_engagement_action": 48,
    "generate_analytics_report": 12,
    "project_monetization": 24,
    "monetization_ideas": 24,
    "suggest_content_category": 24,
    "forecast_viral_potential": 12,
    "generate_content_ideas": 12,
    "classify_intent": 1,
    "caption_generator": 24,
    "hashtag_pack": 24,
    "bio_optimizer": 48,
    "content_calendar": 24,
    "posting_schedule": 48,
    "story_ideas": 24,
    "profile_audit": 48,
    "chat_response": 0,   # never cache conversational responses
}
DEFAULT_TTL = 24


# ── Internal helpers ──────────────────────────────────────────────────────────

def _get_conn() -> sqlite3.Connection:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── Public: initialisation ────────────────────────────────────────────────────

def init_prompt_log_db() -> None:
    """Create logging and cache tables if they do not already exist."""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS prompt_response_logs (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id       INTEGER,
                command       TEXT    NOT NULL,
                prompt_hash   TEXT    NOT NULL,
                prompt_text   TEXT    NOT NULL,
                response_json TEXT,
                success       INTEGER NOT NULL DEFAULT 0,
                error_msg     TEXT,
                latency_ms    INTEGER,
                model         TEXT,
                created_at    TEXT    NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ai_response_cache (
                cache_key    TEXT PRIMARY KEY,
                command      TEXT NOT NULL,
                response_json TEXT NOT NULL,
                hit_count    INTEGER NOT NULL DEFAULT 0,
                created_at   TEXT NOT NULL,
                last_used_at TEXT NOT NULL,
                expires_at   TEXT NOT NULL
            )
        """)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_prl_command  ON prompt_response_logs(command)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_prl_chat_id  ON prompt_response_logs(chat_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_prl_created  ON prompt_response_logs(created_at)"
        )
        conn.commit()
    logger.debug("[DB] prompt_response_logs and ai_response_cache tables ready")


# ── Public: cache key builder ─────────────────────────────────────────────────

def make_cache_key(command: str, **context) -> str:
    """Build a deterministic SHA-256 cache key from command + semantic context.

    Field order is fixed so the same logical request always hashes identically
    regardless of how kwargs are passed.
    """
    parts = [command]
    for field in ("niche", "account_stage", "region", "action", "topic"):
        parts.append(str(context.get(field, "")).lower().strip())
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode()).hexdigest()


# ── Public: logging ───────────────────────────────────────────────────────────

def log_prompt_response(
    command: str,
    prompt_hash: str,
    prompt_text: str,
    success: int,
    latency_ms: int,
    model: str,
    chat_id: int = None,
    response_json: str = None,
    error_msg: str = None,
) -> None:
    """Append one row to prompt_response_logs (fire-and-forget, never raises)."""
    try:
        with _get_conn() as conn:
            conn.execute(
                """
                INSERT INTO prompt_response_logs
                    (chat_id, command, prompt_hash, prompt_text,
                     response_json, success, error_msg, latency_ms, model, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    chat_id, command, prompt_hash, prompt_text,
                    response_json, success, error_msg, latency_ms, model,
                    datetime.utcnow().isoformat(),
                ),
            )
            conn.commit()
    except Exception as exc:
        logger.error("[DB] log_prompt_response failed: %s", exc)


# ── Public: cache read/write ──────────────────────────────────────────────────

def get_cached_response(
    cache_key: str,
    ignore_ttl: bool = False,
) -> Optional[Dict[str, Any]]:
    """Return a parsed response dict for *cache_key*, or ``None`` if not found.

    When *ignore_ttl* is True the lookup ignores the expiry column, allowing
    stale entries to be served as an emergency fallback.
    Bumps ``hit_count`` and ``last_used_at`` on every successful hit.
    """
    try:
        now = datetime.utcnow().isoformat()
        with _get_conn() as conn:
            if ignore_ttl:
                row = conn.execute(
                    "SELECT * FROM ai_response_cache WHERE cache_key = ?",
                    (cache_key,),
                ).fetchone()
            else:
                row = conn.execute(
                    "SELECT * FROM ai_response_cache WHERE cache_key = ? AND expires_at > ?",
                    (cache_key, now),
                ).fetchone()

            if row is None:
                return None

            conn.execute(
                "UPDATE ai_response_cache SET hit_count = hit_count + 1, last_used_at = ? "
                "WHERE cache_key = ?",
                (now, cache_key),
            )
            conn.commit()

        data = json.loads(row["response_json"])
        data["_cache_created_at"] = row["created_at"]
        return data
    except Exception as exc:
        logger.error("[DB] get_cached_response failed: %s", exc)
        return None


def upsert_cache(
    cache_key: str,
    command: str,
    response_json: str,
    ttl_hours: int = None,
) -> None:
    """Insert or replace a cache entry.

    Uses ``COMMAND_TTL[command]`` when *ttl_hours* is not provided.
    Commands with TTL 0 (e.g. chat_response) are never cached.
    """
    ttl = ttl_hours if ttl_hours is not None else COMMAND_TTL.get(command, DEFAULT_TTL)
    if ttl == 0:
        return  # never cache this command type
    now = datetime.utcnow()
    expires_at = (now + timedelta(hours=ttl)).isoformat()
    now_iso = now.isoformat()
    try:
        with _get_conn() as conn:
            conn.execute(
                """
                INSERT INTO ai_response_cache
                    (cache_key, command, response_json, hit_count,
                     created_at, last_used_at, expires_at)
                VALUES (?, ?, ?, 0, ?, ?, ?)
                ON CONFLICT(cache_key) DO UPDATE SET
                    response_json = excluded.response_json,
                    created_at    = excluded.created_at,
                    last_used_at  = excluded.last_used_at,
                    expires_at    = excluded.expires_at
                """,
                (cache_key, command, response_json, now_iso, now_iso, expires_at),
            )
            conn.commit()
    except Exception as exc:
        logger.error("[DB] upsert_cache failed: %s", exc)


def purge_expired_cache() -> int:
    """Delete all rows where ``expires_at`` is in the past.

    Returns the number of rows deleted.
    """
    try:
        now = datetime.utcnow().isoformat()
        with _get_conn() as conn:
            cursor = conn.execute(
                "DELETE FROM ai_response_cache WHERE expires_at < ?", (now,)
            )
            conn.commit()
            deleted = cursor.rowcount
        if deleted:
            logger.info("[DB] Purged %d expired cache entries", deleted)
        return deleted
    except Exception as exc:
        logger.error("[DB] purge_expired_cache failed: %s", exc)
        return 0
