## file to translate csv data into domain language
import csv
from datetime import datetime
from pathlib import Path

from fc26.domain.models import SalePrint


def parse_sale_print_row(row: dict[str, str]) -> SalePrint:
    return SalePrint(
        asset_id=row["asset_id"],
        platform=row["platform"],
        ts_utc=datetime.fromisoformat(row["ts_utc"]),
        price_gross=int(row["price_gross"]),
    )


def read_sale_prints(csv_path: Path) -> list[SalePrint]:
    sale_prints = []

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sale_print = parse_sale_print_row(row)
            sale_prints.append(sale_print)

    return sale_prints
