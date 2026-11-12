import sqlite3
from pathlib import Path

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
