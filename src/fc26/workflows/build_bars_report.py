from fc26.domain.models import Bar
from fc26.features.bars import build_bars
from fc26.storage.db import init_db
from fc26.storage.sale_print_repo import get_sale_prints


def get_bars(asset_id, platform, timeframe_minutes) -> list[Bar]:
    conn = init_db()
    try:
        sale_prints = get_sale_prints(conn, asset_id, platform)
        bars = build_bars(sale_prints, timeframe_minutes)
        return bars
    finally:
        conn.close()
