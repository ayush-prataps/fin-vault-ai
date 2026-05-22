"""Simple SQL migration runner.

Scans `db/migrations/` for *.sql files sorted by name and applies any that
haven't been recorded in `schema_migrations` table. This is idempotent and
safe to call at application startup.
"""
from pathlib import Path
from datetime import datetime
from typing import List
from app.core.db import get_db_connection


MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "db" / "migrations"


def ensure_migrations_table(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                filename VARCHAR(255) PRIMARY KEY,
                applied_at TIMESTAMP NOT NULL
            );
            """
        )


def list_migration_files() -> List[Path]:
    if not MIGRATIONS_DIR.exists():
        return []
    files = sorted([p for p in MIGRATIONS_DIR.iterdir() if p.suffix == ".sql"])
    return files


def applied_migrations(conn) -> List[str]:
    with conn.cursor() as cur:
        cur.execute("SELECT filename FROM schema_migrations")
        return [r[0] for r in cur.fetchall()]


def apply_migration_file(conn, path: Path):
    sql = path.read_text()
    with conn.cursor() as cur:
        cur.execute(sql)
        cur.execute("INSERT INTO schema_migrations (filename, applied_at) VALUES (%s, %s) ON CONFLICT DO NOTHING", (path.name, datetime.utcnow()))


def apply_migrations():
    files = list_migration_files()
    if not files:
        return 0

    with get_db_connection() as conn:
        ensure_migrations_table(conn)
        applied = set(applied_migrations(conn))
        to_apply = [f for f in files if f.name not in applied]
        if not to_apply:
            return 0

        count = 0
        for f in to_apply:
            try:
                apply_migration_file(conn, f)
                conn.commit()
                count += 1
            except Exception:
                conn.rollback()
                raise

    return count
