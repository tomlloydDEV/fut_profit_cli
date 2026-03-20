import sqlite3
from datetime import datetime

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


def get_sale_prints(conn, asset_id, platform):
    cursor = conn.execute(
        """
        SELECT asset_id, platform, ts_utc, price_gross
        FROM sale_prints
        WHERE asset_id = ? AND platform = ?
        ORDER BY ts_utc ASC
        """,
        (asset_id, platform),
    )

    rows = cursor.fetchall()

    sale_prints = []

    for row in rows:
        sale_print = SalePrint(
            asset_id=row[0],
            platform=row[1],
            ts_utc=datetime.fromisoformat(row[2]),
            price_gross=row[3],
        )
        sale_prints.append(sale_print)

    return sale_prints


# temp
if __name__ == "__main__":
    print("RUNNER STARTED")
    from fc26.storage.db import init_db

    conn = init_db()

    sale_prints = get_sale_prints(
        conn,
        asset_id="mctominay-fut-birthday",
        platform="ps",
    )

    print("RESULT:", sale_prints)

    conn.close()
