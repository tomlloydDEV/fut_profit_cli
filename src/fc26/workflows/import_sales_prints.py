from pathlib import Path

from fc26.ingest import csv_parser
from fc26.ingest.csv_parser import read_sale_prints
from fc26.storage.db import init_db
from fc26.storage.sale_print_repo import insert_sale_print


def import_sales_prints_from_csv(csv_path: Path) -> int:
    conn = init_db()
    sales_prints = read_sale_prints(csv_path)

    for sale_print in sales_prints:
        insert_sale_print(conn, sale_print)

    conn.close()
    return len(sales_prints)


if __name__ == "__main__":
    csv_path = Path("data/fixtures/mctominay_fut_birthday_sales.csv")

    imported_count = import_sales_prints_from_csv(csv_path)

    print(f"Imported {imported_count} sales prints from {csv_path}")
