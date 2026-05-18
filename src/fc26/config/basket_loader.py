from pathlib import Path

import yaml

from fc26.domain.models import Basket, BasketAsset


def load_basket(path: str | Path) -> Basket:
    path = Path(path)

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))

    assets = []

    for raw_asset in raw["assets"]:
        asset = BasketAsset(
            asset_id=raw_asset["asset_id"],
            futbin_id=raw_asset.get("futbin_id"),
            name=raw_asset["name"],
            version=raw_asset.get("version"),
            role=raw_asset.get("role"),
            notes=raw_asset.get("notes"),
        )

        assets.append(asset)

    return Basket(
        name=raw["name"],
        basket_type=raw["basket_type"],
        platform=raw["platform"],
        description=raw.get("description"),
        assets=assets,
    )


if __name__ == "__main__":
    basket = load_basket("baskets/rhythm.yaml")

    print(basket.name)
    print(basket.basket_type)
    print(basket.platform)

    for asset in basket.assets:
        print("-", asset.asset_id, asset.name)
        )
