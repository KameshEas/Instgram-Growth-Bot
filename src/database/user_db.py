"""
SQLite-backed user profile store.

Uses only the stdlib ``sqlite3`` module — no additional dependencies.
DB file is created automatically on first use.
"""

import sqlite3
import json
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Resolve DB path: env var > default next to project root
_DEFAULT_DB = str(Path(__file__).parent.parent.parent / "data" / "users.db")
DB_PATH: str = os.getenv("SQLITE_DB_PATH", _DEFAULT_DB)


def _get_conn() -> sqlite3.Connection:
    """Return a connection with row_factory set to Row for dict-like access."""
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the user_profiles table if it doesn't exist yet."""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                chat_id       INTEGER PRIMARY KEY,
                username      TEXT,
                niche         TEXT,
                audience_size TEXT,
                goals_json    TEXT DEFAULT '[]',
                settings_json TEXT DEFAULT '{}',
                created_at    TEXT,
                updated_at    TEXT
            )
        """)
        # Migrate existing users by adding settings_json column if missing
        try:
            conn.execute("ALTER TABLE user_profiles ADD COLUMN settings_json TEXT DEFAULT '{}'")
        except sqlite3.OperationalError:
            pass  # Column already exists
        conn.commit()
    logger.debug("[DB] user_profiles table ready at %s", DB_PATH)


def get_profile(chat_id: int) -> Optional[Dict[str, Any]]:
    """Return the profile dict for *chat_id*, or ``None`` if not found."""
    init_db()
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM user_profiles WHERE chat_id = ?", (chat_id,)
        ).fetchone()
    if row is None:
        return None
    data = dict(row)
    data["goals"] = json.loads(data.pop("goals_json", "[]") or "[]")
    data["settings"] = json.loads(data.pop("settings_json", "{}") or "{}")
    return data


def save_profile(
    chat_id: int,
    username: Optional[str] = None,
    niche: Optional[str] = None,
    audience_size: Optional[str] = None,
    goals: Optional[list] = None,
    settings: Optional[dict] = None,
) -> Dict[str, Any]:
    """Insert or fully replace the profile for *chat_id*.  Returns the saved profile."""
    init_db()
    now = datetime.utcnow().isoformat()
    with _get_conn() as conn:
        conn.execute(
            """
            INSERT INTO user_profiles
                (chat_id, username, niche, audience_size, goals_json, settings_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET
                username      = excluded.username,
                niche         = excluded.niche,
                audience_size = excluded.audience_size,
                goals_json    = excluded.goals_json,
                settings_json = excluded.settings_json,
                updated_at    = excluded.updated_at
            """,
            (
                chat_id,
                username,
                niche,
                audience_size,
                json.dumps(goals or []),
                json.dumps(settings or {}),
                now,
                now,
            ),
        )
        conn.commit()
    logger.debug("[DB] Profile saved for chat_id=%s", chat_id)
    return get_profile(chat_id)


def update_profile(chat_id: int, **kwargs) -> Optional[Dict[str, Any]]:
    """Partially update one or more fields for *chat_id*.

    Accepted keyword args: ``username``, ``niche``, ``audience_size``, ``goals``, ``settings``.
    Returns the updated profile or ``None`` if the user does not exist yet.
    """
    profile = get_profile(chat_id)
    if profile is None:
        return None
    # Merge updates into existing values
    username = kwargs.get("username", profile.get("username"))
    niche = kwargs.get("niche", profile.get("niche"))
    audience_size = kwargs.get("audience_size", profile.get("audience_size"))
    goals = kwargs.get("goals", profile.get("goals", []))
    settings = kwargs.get("settings", profile.get("settings", {}))
    return save_profile(
        chat_id,
        username=username,
        niche=niche,
        audience_size=audience_size,
        goals=goals,
        settings=settings,
    )


def delete_profile(chat_id: int) -> None:
    """Remove the profile for *chat_id* (used by /profile reset)."""
    init_db()
    with _get_conn() as conn:
        conn.execute("DELETE FROM user_profiles WHERE chat_id = ?", (chat_id,))
        conn.commit()
    logger.debug("[DB] Profile deleted for chat_id=%s", chat_id)


def get_user_settings(chat_id: int) -> Dict[str, Any]:
    """Get user settings (niche, region, follower_count, account_stage, language, etc.)."""
    profile = get_profile(chat_id)
    if not profile:
        return {}
    return profile.get("settings", {})


def update_user_settings(chat_id: int, **settings) -> Dict[str, Any]:
    """Update user settings. Merges with existing settings.
    
    Example:
        update_user_settings(12345, niche="fitness", region="US", follower_count=50000)
    """
    current = get_user_settings(chat_id)
    current.update(settings)
    return update_profile(chat_id, settings=current)


def save_user_settings(
    chat_id: int,
    niche: Optional[str] = None,
    region: Optional[str] = None,
    follower_count: Optional[int] = None,
    account_stage: Optional[str] = None,
    language: Optional[str] = None,
    engagement_rate: Optional[float] = None,
    content_mix: Optional[list] = None,
) -> Dict[str, Any]:
    """Convenience method to save common user settings."""
    settings_dict = {}
    if niche is not None:
        settings_dict["niche"] = niche
    if region is not None:
        settings_dict["region"] = region
    if follower_count is not None:
        settings_dict["follower_count"] = follower_count
    if account_stage is not None:
        settings_dict["account_stage"] = account_stage
    if language is not None:
        settings_dict["language"] = language
    if engagement_rate is not None:
        settings_dict["engagement_rate"] = engagement_rate
    if content_mix is not None:
        settings_dict["content_mix"] = content_mix
    return update_user_settings(chat_id, **settings_dict)

