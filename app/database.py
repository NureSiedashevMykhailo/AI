import sqlite3
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = "data/app.db"

UPDATABLE_ISSUE_COLUMNS = frozenset({"title", "description", "priority", "assignee_id"})

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


def list_users(db_path: str | Path) -> list[dict[str, Any]]:
    """Return all predefined users ordered by id ASC."""
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            """
            SELECT id, name
            FROM users
            ORDER BY id ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]
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


def _fetch_issue_row(
    conn: sqlite3.Connection,
    issue_id: int,
) -> dict[str, Any] | None:
    try:
        row = conn.execute(
            """
            SELECT id, title, description, status, priority, assignee_id, created_at
            FROM issues
            WHERE id = ?
            """,
            (issue_id,),
        ).fetchone()
    except OverflowError:
        return None
    return dict(row) if row is not None else None


def get_issue_by_id(db_path: str | Path, issue_id: int) -> dict[str, Any] | None:
    """Fetch a single issue by id, or return None if not found."""
    conn = get_connection(db_path)
    try:
        return _fetch_issue_row(conn, issue_id)
    finally:
        conn.close()


def update_issue(
    db_path: str | Path,
    issue_id: int,
    updates: dict[str, Any],
) -> dict[str, Any] | None:
    """Atomically update allowed fields of an existing issue and return it."""
    if not updates:
        return get_issue_by_id(db_path, issue_id)

    invalid_columns = set(updates) - UPDATABLE_ISSUE_COLUMNS
    if invalid_columns:
        raise ValueError(f"Unsupported issue columns: {sorted(invalid_columns)}")

    assignments = ", ".join(f"{column} = ?" for column in updates)
    params = [*updates.values(), issue_id]

    conn = get_connection(db_path)
    try:
        try:
            with conn:
                cursor = conn.execute(
                    f"UPDATE issues SET {assignments} WHERE id = ?",
                    params,
                )
                if cursor.rowcount == 0:
                    return None
        except OverflowError:
            return None
        return _fetch_issue_row(conn, issue_id)
    finally:
        conn.close()


def update_issue_status(
    db_path: str | Path,
    issue_id: int,
    new_status: str,
) -> dict[str, Any] | None:
    """Atomically update the status of an existing issue and return it."""
    conn = get_connection(db_path)
    try:
        try:
            with conn:
                cursor = conn.execute(
                    "UPDATE issues SET status = ? WHERE id = ?",
                    (new_status, issue_id),
                )
                if cursor.rowcount == 0:
                    return None
        except OverflowError:
            return None
        return _fetch_issue_row(conn, issue_id)
    finally:
        conn.close()


def insert_comment(
    db_path: str | Path,
    *,
    issue_id: int,
    author_id: int,
    text: str,
    created_at: str,
) -> dict[str, Any]:
    """Insert a new comment row and return the persisted record."""
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO comments (issue_id, author_id, text, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (issue_id, author_id, text, created_at),
            )
            comment_id = cursor.lastrowid
        row = conn.execute(
            """
            SELECT id, issue_id, author_id, text, created_at
            FROM comments
            WHERE id = ?
            """,
            (comment_id,),
        ).fetchone()
        return dict(row)
    finally:
        conn.close()


def list_comments(db_path: str | Path, issue_id: int) -> list[dict[str, Any]]:
    """Return comments for an issue ordered by created_at ASC, id ASC."""
    conn = get_connection(db_path)
    try:
        try:
            rows = conn.execute(
                """
                SELECT id, issue_id, author_id, text, created_at
                FROM comments
                WHERE issue_id = ?
                ORDER BY created_at ASC, id ASC
                """,
                (issue_id,),
            ).fetchall()
        except OverflowError:
            return []
        return [dict(row) for row in rows]
    finally:
        conn.close()
