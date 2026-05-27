from datetime import datetime, timezone

from fc26.domain.models import Bar
from fc26.features.activity_index import build_activity_index


def test_build_activity_index_sums_volume_by_window():
    bars_by_asset = {
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

    points = build_activity_index(
        bars_by_asset=bars_by_asset,
        basket_name="rhythm_test",
        platform="ps",
        timeframe="15m",
    )

    assert len(points) == 2

    first = points[0]
    second = points[1]

    assert first.activity_index == 9
    assert first.asset_count == 3
    assert first.active_asset_count == 2

    assert second.activity_index == 5
    assert second.asset_count == 3
    assert second.active_asset_count == 2
