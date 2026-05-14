import sqlite3
from pathlib import Path

DB_PATH = Path("data/fc26.sqlite")


def get_db_connection(db_path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    return conn


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sale_prints (
            asset_id TEXT NOT NULL,
            platform TEXT NOT NULL,
            ts_utc INTEGER NOT NULL,
            price_gross INTEGET NOT NULL
        )
    """
    )
    conn.commit()


def init_db(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = get_db_connection(db_path)
    ensure_schema(conn)
    return conn
