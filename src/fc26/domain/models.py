from dataclasses import dataclass
from datetime import datetime


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
