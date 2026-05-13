from pickletools import dis

from fc26.domain.models import Bar, SalePrint


def build_bars(sale_prints: list[SalePrint], timeframe_minutes: int) -> list[Bar]:
    bars = []
    buckets = {}

    for sale_print in sale_prints:
        ts = sale_print.ts_utc
        total_minutes = ts.hour * 60 + ts.minute
        bucket_total_minutes = (total_minutes // timeframe_minutes) * timeframe_minutes

        bucket_hour = bucket_total_minutes // 60
        bucket_minute = bucket_total_minutes % 60

        bucket_start = ts.replace(
            hour=bucket_hour,
            minute=bucket_minute,
            second=0,
            microsecond=0,
        )

        if bucket_start not in buckets:
            buckets[bucket_start] = []

        buckets[bucket_start].append(sale_print)

    for bucket_start in sorted(buckets):
        bucket_sale_prints = buckets[bucket_start]

        open_price = bucket_sale_prints[0].price_gross
        high_price = max(sp.price_gross for sp in bucket_sale_prints)
        low_price = min(sp.price_gross for sp in bucket_sale_prints)
        dispersion = high_price - low_price
        close_price = bucket_sale_prints[-1].price_gross
        volume = len(bucket_sale_prints)

        bar = Bar(
            asset_id=bucket_sale_prints[0].asset_id,
            platform=bucket_sale_prints[0].platform,
            timeframe=f"{timeframe_minutes}m",
            window_start_utc=bucket_start,
            open=open_price,
            high=high_price,
            low=low_price,
            close=close_price,
            volume=volume,
            dispersion=dispersion,
        )
        bars.append(bar)

    return bars


# test
if __name__ == "__main__":
    from fc26.storage.db import init_db
    from fc26.storage.sale_print_repo import get_sale_prints

    conn = init_db()

    sale_prints = get_sale_prints(
        conn,
        asset_id="arda-guler-fantasy-fc",
        platform="ps",
    )

    bars = build_bars(sale_prints, 240)

    print("RUNNER STARTED")
    print(f"Built {len(bars)} bars")

    for bar in bars:
        print(bar)

    conn.close()
