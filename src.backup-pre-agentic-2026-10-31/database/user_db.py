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


# ── PHASE 2: Favorites & History ──────────────────────────────────────────

def init_favorites_and_history() -> None:
    """Create favorites and history tables if they don't exist."""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id     INTEGER NOT NULL,
                category    TEXT NOT NULL,
                title       TEXT,
                prompt      TEXT NOT NULL,
                style       TEXT,
                negative_prompt TEXT,
                aspect_ratio TEXT,
                keywords_json TEXT DEFAULT '[]',
                created_at  TEXT,
                updated_at  TEXT,
                FOREIGN KEY(chat_id) REFERENCES user_profiles(chat_id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS prompt_history (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id     INTEGER NOT NULL,
                category    TEXT NOT NULL,
                user_input  TEXT,
                prompt_count INTEGER DEFAULT 3,
                created_at  TEXT,
                FOREIGN KEY(chat_id) REFERENCES user_profiles(chat_id)
            )
        """)
        conn.commit()
    logger.debug("[DB] Favorites and history tables ready")


def save_favorite(
    chat_id: int,
    category: str,
    prompt: str,
    title: Optional[str] = None,
    style: Optional[str] = None,
    negative_prompt: Optional[str] = None,
    aspect_ratio: Optional[str] = None,
    keywords: Optional[list] = None,
) -> Dict[str, Any]:
    """Save a prompt to user's favorites."""
    init_favorites_and_history()
    now = datetime.utcnow().isoformat()
    with _get_conn() as conn:
        conn.execute(
            """
            INSERT INTO favorites
                (chat_id, category, title, prompt, style, negative_prompt, aspect_ratio, keywords_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                chat_id,
                category,
                title,
                prompt,
                style,
                negative_prompt,
                aspect_ratio,
                json.dumps(keywords or []),
                now,
                now,
            ),
        )
        conn.commit()
        fav_id = conn.lastrowid
    logger.debug("[DB] Favorite saved (id=%s) for chat_id=%s", fav_id, chat_id)
    return get_favorite(fav_id)


def get_favorite(fav_id: int) -> Optional[Dict[str, Any]]:
    """Get a favorite by ID."""
    init_favorites_and_history()
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM favorites WHERE id = ?", (fav_id,)
        ).fetchone()
    if row is None:
        return None
    data = dict(row)
    data["keywords"] = json.loads(data.pop("keywords_json", "[]") or "[]")
    return data


def get_user_favorites(chat_id: int, limit: int = 10) -> list:
    """Get all favorites for a user (most recent first)."""
    init_favorites_and_history()
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM favorites WHERE chat_id = ? ORDER BY created_at DESC LIMIT ?",
            (chat_id, limit),
        ).fetchall()
    favorites = []
    for row in rows:
        data = dict(row)
        data["keywords"] = json.loads(data.pop("keywords_json", "[]") or "[]")
        favorites.append(data)
    return favorites


def delete_favorite(fav_id: int) -> None:
    """Remove a favorite by ID."""
    init_favorites_and_history()
    with _get_conn() as conn:
        conn.execute("DELETE FROM favorites WHERE id = ?", (fav_id,))
        conn.commit()
    logger.debug("[DB] Favorite deleted (id=%s)", fav_id)


def save_history(
    chat_id: int,
    category: str,
    user_input: Optional[str] = None,
    prompt_count: int = 3,
) -> Dict[str, Any]:
    """Record a prompt generation in user's history."""
    init_favorites_and_history()
    now = datetime.utcnow().isoformat()
    with _get_conn() as conn:
        conn.execute(
            """
            INSERT INTO prompt_history
                (chat_id, category, user_input, prompt_count, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (chat_id, category, user_input, prompt_count, now),
        )
        conn.commit()
        hist_id = conn.lastrowid
    logger.debug("[DB] History recorded (id=%s) for chat_id=%s", hist_id, chat_id)
    return get_history_entry(hist_id)


def get_history_entry(hist_id: int) -> Optional[Dict[str, Any]]:
    """Get a history entry by ID."""
    init_favorites_and_history()
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM prompt_history WHERE id = ?", (hist_id,)
        ).fetchone()
    return dict(row) if row else None


def get_user_history(chat_id: int, limit: int = 20) -> list:
    """Get user's prompt generation history (most recent first)."""
    init_favorites_and_history()
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM prompt_history WHERE chat_id = ? ORDER BY created_at DESC LIMIT ?",
            (chat_id, limit),
        ).fetchall()
    return [dict(row) for row in rows]


def clear_user_history(chat_id: int) -> None:
    """Clear all history for a user."""
    init_favorites_and_history()
    with _get_conn() as conn:
        conn.execute("DELETE FROM prompt_history WHERE chat_id = ?", (chat_id,))
        conn.commit()
    logger.debug("[DB] History cleared for chat_id=%s", chat_id)


# ── PHASE 3: Smart Analytics & Recommendations ─────────────────────────────

def get_favorite_by_id(fav_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific favorite by ID (includes full metadata)."""
    init_favorites_and_history()
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM favorites WHERE id = ?", (fav_id,)
        ).fetchone()
    if row is None:
        return None
    data = dict(row)
    data["keywords"] = json.loads(data.pop("keywords_json", "[]") or "[]")
    return data


def search_favorites(chat_id: int, keyword: str, limit: int = 10) -> list:
    """Search user's favorites by keyword (searches title, style, prompt)."""
    init_favorites_and_history()
    search_term = f"%{keyword}%"
    with _get_conn() as conn:
        rows = conn.execute(
            """SELECT * FROM favorites
               WHERE chat_id = ? AND (
                   title LIKE ? OR
                   style LIKE ? OR
                   prompt LIKE ? OR
                   keywords_json LIKE ?
               )
               ORDER BY created_at DESC LIMIT ?""",
            (chat_id, search_term, search_term, search_term, search_term, limit),
        ).fetchall()
    favorites = []
    for row in rows:
        data = dict(row)
        data["keywords"] = json.loads(data.pop("keywords_json", "[]") or "[]")
        favorites.append(data)
    return favorites


def get_favorites_by_category(chat_id: int, category: str, limit: int = 10) -> list:
    """Get all favorites in a specific category."""
    init_favorites_and_history()
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM favorites WHERE chat_id = ? AND category = ? ORDER BY created_at DESC LIMIT ?",
            (chat_id, category, limit),
        ).fetchall()
    favorites = []
    for row in rows:
        data = dict(row)
        data["keywords"] = json.loads(data.pop("keywords_json", "[]") or "[]")
        favorites.append(data)
    return favorites


def get_category_stats(chat_id: int) -> Dict[str, int]:
    """Get statistics on favorite categories (most common first)."""
    init_favorites_and_history()
    with _get_conn() as conn:
        rows = conn.execute(
            """SELECT category, COUNT(*) as count FROM favorites
               WHERE chat_id = ?
               GROUP BY category
               ORDER BY count DESC""",
            (chat_id,),
        ).fetchall()
    stats = {row["category"]: row["count"] for row in rows}
    return stats


def get_generation_stats(chat_id: int) -> Dict[str, Any]:
    """Get statistics on user's generation activity."""
    init_favorites_and_history()
    with _get_conn() as conn:
        # Total generations
        total = conn.execute(
            "SELECT COUNT(*) as count FROM prompt_history WHERE chat_id = ?",
            (chat_id,),
        ).fetchone()

        # Most used categories
        categories = conn.execute(
            """SELECT category, COUNT(*) as count FROM prompt_history
               WHERE chat_id = ?
               GROUP BY category
               ORDER BY count DESC LIMIT 5""",
            (chat_id,),
        ).fetchall()

        # Total favorites
        fav_count = conn.execute(
            "SELECT COUNT(*) as count FROM favorites WHERE chat_id = ?",
            (chat_id,),
        ).fetchone()

    return {
        "total_generations": total["count"] if total else 0,
        "favorite_categories": {row["category"]: row["count"] for row in categories},
        "total_favorites": fav_count["count"] if fav_count else 0,
        "favorite_rate": f"{(fav_count['count'] / max(total['count'], 1) * 100):.1f}%" if total and total["count"] > 0 else "0%",
    }


def get_most_used_categories(chat_id: int, limit: int = 5) -> list:
    """Get user's most frequently generated categories."""
    init_favorites_and_history()
    with _get_conn() as conn:
        rows = conn.execute(
            """SELECT category, COUNT(*) as count FROM prompt_history
               WHERE chat_id = ?
               GROUP BY category
               ORDER BY count DESC LIMIT ?""",
            (chat_id, limit),
        ).fetchall()
    return [(row["category"], row["count"]) for row in rows]


def get_smart_recommendations(chat_id: int) -> list:
    """Get smart category recommendations based on user's history."""
    init_favorites_and_history()

    # Get categories user has generated most
    with _get_conn() as conn:
        most_used = conn.execute(
            """SELECT category FROM prompt_history
               WHERE chat_id = ?
               GROUP BY category
               ORDER BY COUNT(*) DESC LIMIT 3""",
            (chat_id,),
        ).fetchall()

    recommendations = [row["category"] for row in most_used]

    # If user has favorites, also suggest related categories
    if recommendations:
        return recommendations

    # If no history, return popular starters
    return ["general_photography", "women_professional", "design_posters"]


def get_last_generation(chat_id: int) -> Optional[Dict[str, Any]]:
    """Get the user's most recent generation for quick regenerate."""
    init_favorites_and_history()
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM prompt_history WHERE chat_id = ? ORDER BY created_at DESC LIMIT 1",
            (chat_id,),
        ).fetchone()
    return dict(row) if row else None


def count_user_favorites(chat_id: int) -> int:
    """Count total favorites for a user."""
    init_favorites_and_history()
    with _get_conn() as conn:
        result = conn.execute(
            "SELECT COUNT(*) as count FROM favorites WHERE chat_id = ?",
            (chat_id,),
        ).fetchone()
    return result["count"] if result else 0


def count_user_history(chat_id: int) -> int:
    """Count total history entries for a user."""
    init_favorites_and_history()
    with _get_conn() as conn:
        result = conn.execute(
            "SELECT COUNT(*) as count FROM prompt_history WHERE chat_id = ?",
            (chat_id,),
        ).fetchone()
    return result["count"] if result else 0

