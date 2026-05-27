from collections import defaultdict
from datetime import datetime
from sys import flags

from fc26.domain.models import ActivityIndexPoint, Bar


def build_activity_index(
    bars_by_asset: dict[str, list[Bar]],
    basket_name: str,
    platform: str,
    timeframe: str,
) -> list[ActivityIndexPoint]:
    volume_by_window: defaultdict[datetime, int] = defaultdict(int)
    active_assets_by_window: defaultdict[datetime, set[str]] = defaultdict(set)

    asset_count = len(bars_by_asset)

    for asset_id, bars in bars_by_asset.items():
        for bar in bars:
            window_start = bar.window_start_utc

            volume_by_window[window_start] += bar.volume
            active_assets_by_window[window_start].add(asset_id)

    activity_points: list[ActivityIndexPoint] = []

    for window_start in sorted(volume_by_window):
        activity_index = volume_by_window[window_start]

        point = ActivityIndexPoint(
            basket_name=basket_name,
            platform=platform,
            timeframe=timeframe,
            window_start_utc=window_start,
            activity_index=activity_index,
            asset_count=asset_count,
            active_asset_count=len(active_assets_by_window[window_start]),
        )

        activity_points.append(point)

    return activity_points


if __name__ == "__main__":
    from datetime import datetime, timezone

    fake_bars_by_asset = {
        "dembele_gold": [
            Bar(
                asset_id="dembele_gold",
                platform="ps",
                timeframe="15m",
                window_start_utc=datetime(2026, 3, 26, 15, 0, tzinfo=timezone.utc),
                open=100_000,
                high=102_000,
                low=99_000,
                close=101_000,
                volume=5,
                dispersion=3_000,
            ),
            Bar(
                asset_id="dembele_gold",
                platform="ps",
                timeframe="15m",
                window_start_utc=datetime(2026, 3, 26, 15, 15, tzinfo=timezone.utc),
                open=101_000,
                high=103_000,
                low=100_000,
                close=102_000,
                volume=3,
                dispersion=3_000,
            ),
        ],
        "valverde_gold": [
            Bar(
                asset_id="valverde_gold",
                platform="ps",
                timeframe="15m",
                window_start_utc=datetime(2026, 3, 26, 15, 0, tzinfo=timezone.utc),
                open=80_000,
                high=81_000,
                low=79_500,
                close=80_500,
                volume=4,
                dispersion=1_500,
            ),
        ],
        "theo_hernandez_gold": [
            Bar(
                asset_id="theo_hernandez_gold",
                platform="ps",
                timeframe="15m",
                window_start_utc=datetime(2026, 3, 26, 15, 15, tzinfo=timezone.utc),
                open=120_000,
                high=121_000,
                low=119_000,
                close=120_500,
                volume=2,
                dispersion=2_000,
            ),
        ],
    }

    activity_points = build_activity_index(
        bars_by_asset=fake_bars_by_asset,
        basket_name="rhythm_test",
        platform="ps",
        timeframe="15m",
    )

    for point in activity_points:
        print(point)
