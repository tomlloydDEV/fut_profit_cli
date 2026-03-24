from fc26.domain.models import Bar, SalePrint


def build_bars(sale_prints: list[SalePrint], timeframe_minutes: int) -> list[Bar]:
    bars = []
    buckets = {}

    for sale_print in sale_prints:
        ts = sale_print.ts_utc
        bucket_minute = (ts.minute // timeframe_minutes) * timeframe_minutes
        bucket_start = ts.replace(minute=bucket_minute, second=0, microsecond=0)

        if bucket_start not in buckets:
            buckets[bucket_start] = []

        buckets[bucket_start].append(sale_print)

    for bucket_start, bucket_sale_prints in buckets.items():
        print(bucket_start, len(bucket_sale_prints))

    return bars
