from pathlib import Path

import yaml

from fc26.domain.models import Basket, BasketAsset

VALID_BASKET_TYPES = {"rhythm", "oppurtunity", "peer", "sentinel"}


class BasketLoadError(ValueError):
    """Raised when the basket type is not valid."""


def load_basket(path: str | Path) -> Basket:
    path = Path(path)

    if not path.exists():
        raise BasketLoadError(f"Basket file does not exist: {path}")

    try:
        text = path.read_text(encoding="utf-8")
        raw = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise BasketLoadError(f"Invalid YAML in basket file: {exc}") from exc

    if raw is None:
        raise BasketLoadError("Basket file is empty or invalid")

    if not isinstance(raw, dict):
        raise BasketLoadError(
            f"Basket file must contain a YAML object at the top level: {path}"
        )

    name = raw["name"]
    basket_type = raw["basket_type"]
    platform = raw["platform"]
    description = raw["description"]

    if basket_type not in VALID_BASKET_TYPES:
        raise BasketLoadError(
            f"Invalid basket type: {basket_type}"
            f"Expected one of: {sorted(VALID_BASKET_TYPES)}"
        )

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
        name=name,
        basket_type=basket_type,
        platform=platform,
        description=description,
        assets=assets,
    )


if __name__ == "__main__":
    basket = load_basket("baskets/rhythm.yaml")

    print(basket.name)
    print(basket.basket_type)
    print(basket.platform)

    for asset in basket.assets:
        print("-", asset.asset_id, asset.name)
