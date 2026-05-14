from dataclasses import dataclass, field
from datetime import datetime
from pydoc import plainpager


@dataclass
class SalePrint:
    asset_id: str
    platform: str
    ts_utc: datetime
    price_gross: int


@dataclass
class Bar:
    asset_id: str
    platform: str
    timeframe: str
    window_start_utc: datetime
    open: int
    high: int
    low: int
    close: int
    volume: int
    dispersion: int


@dataclass
class BasketAsset:
    asset_id: str
    futbin_id: str | None
    name: str
    version: str | None = None
    role: str | None = None
    notes: str | None = None


@dataclass(frozen=True)
class Basket:
    name: str
    basket_type: str
    platform: str
    assets: list[BasketAsset]
    description: str | None = None
    metadata: dict = field(default_factory=dict)
