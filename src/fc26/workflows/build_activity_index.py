from fc26.config.basket_loader import load_basket
from fc26.features.activity_index import build_activity_index
from fc26.workflows.build_bars_report import get_bars


def get_activity_index_report(
    basket_path: str,
    timeframe_minutes: int,
):
    basket = load_basket(basket_path)

    bars_by_asset = {}

    print(f"Loaded basket: {basket.name}")
    print(f"Basket type: {basket.basket_type}")
    print(f"Platform: {basket.platform}")
    print(f"Assets in basket: {len(basket.assets)}")
    print()

    for asset in basket.assets:
        bars = get_bars(
            asset_id=asset.asset_id,
            platform=basket.platform,
            timeframe_minutes=timeframe_minutes,
        )

        bars_by_asset[asset.asset_id] = bars

        print(f"{asset.asset_id}: {len(bars)} bars")

    print()

    activity_points = build_activity_index(
        bars_by_asset=bars_by_asset,
        basket_name=basket.name,
        platform=basket.platform,
        timeframe=f"{timeframe_minutes}m",
    )

    return activity_points


def print_activity_index_report(activity_points):
    print("ActivityIndex report")
    print("====================")
    print(f"Points built: {len(activity_points)}")
    print()

    if not activity_points:
        print("No ActivityIndex points were built.")
        print()
        print("Most likely reason:")
        print(
            "- The basket asset_id values do not match assets currently stored in SQLite."
        )
        print("- Or those assets have no sale prints imported yet.")
        return

    print("First 20 ActivityIndex points:")
    print()

    for point in activity_points[:20]:
        print(
            f"{point.window_start_utc} | "
            f"activity_index={point.activity_index} | "
            f"active_assets={point.active_asset_count}/{point.asset_count}"
        )


if __name__ == "__main__":
    points = get_activity_index_report(
        basket_path="baskets/rhythm.yaml",
        timeframe_minutes=15,
    )

    print_activity_index_report(points)
