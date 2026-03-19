import sqlite3

from fc26.domain.models import SalePrint


def insert_sale_print(conn: sqlite3.Connection, sale_print: SalePrint) -> None:
    conn.execute(
        """
    INSERT INTO sale_prints (
    asset_id,
    platform,
    ts_utc,
    price_gross
    )
    VALUES (?, ?, ?, ?)
    """,
        (
            sale_print.asset_id,
            sale_print.platform,
            sale_print.ts_utc.isoformat(),
            sale_print.price_gross,
        ),
    )
    conn.commit()
