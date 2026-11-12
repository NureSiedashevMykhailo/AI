import sqlite3
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = "data/app.db"

SEED_USERS: tuple[tuple[int, str], ...] = (
    (1, "Agent A"),
    (2, "Agent B"),
)


def get_connection(db_path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Open a SQLite connection with foreign keys enabled and Row factory."""
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: str | Path = DEFAULT_DB_PATH) -> None:
    """Initialize SQLite schema and idempotently seed predefined users."""
    db_path_str = str(db_path)
    if db_path_str != ":memory:" and not db_path_str.startswith("file:"):
        Path(db_path_str).parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection(db_path_str)
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'OPEN'
                        CHECK (status IN ('OPEN', 'IN_PROGRESS', 'CLOSED')),
                    priority TEXT NOT NULL DEFAULT 'medium'
                        CHECK (priority IN ('low', 'medium', 'high')),
                    assignee_id INTEGER NULL REFERENCES users(id),
                    created_at TEXT NOT NULL
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    issue_id INTEGER NOT NULL REFERENCES issues(id),
                    author_id INTEGER NOT NULL REFERENCES users(id),
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )
            conn.executemany(
                "INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)",
                SEED_USERS,
            )
    finally:
        conn.close()


def insert_issue(
    db_path: str | Path,
    *,
    title: str,
    description: str,
    status: str,
    priority: str,
    assignee_id: int | None,
    created_at: str,
) -> dict[str, Any]:
    """Insert a new issue row and return the persisted record."""
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO issues (
                    title,
                    description,
                    status,
                    priority,
                    assignee_id,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (title, description, status, priority, assignee_id, created_at),
            )
            issue_id = cursor.lastrowid
        row = conn.execute(
            """
            SELECT id, title, description, status, priority, assignee_id, created_at
            FROM issues
            WHERE id = ?
            """,
            (issue_id,),
        ).fetchone()
        return dict(row)
    finally:
        conn.close()


def list_issues(db_path: str | Path) -> list[dict[str, Any]]:
    """Return all issues ordered chronologically by created_at ASC, id ASC."""
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            """
            SELECT id, title, description, status, priority, assignee_id, created_at
            FROM issues
            ORDER BY created_at ASC, id ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_issue_by_id(db_path: str | Path, issue_id: int) -> dict[str, Any] | None:
    """Fetch a single issue by id, or return None if not found."""
    conn = get_connection(db_path)
    try:
        row = conn.execute(
            """
            SELECT id, title, description, status, priority, assignee_id, created_at
            FROM issues
            WHERE id = ?
            """,
            (issue_id,),
        ).fetchone()
        return dict(row) if row is not None else None
    finally:
        conn.close()
