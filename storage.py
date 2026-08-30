import csv

from config import CSV_FILE, CSV_HEADER, color, GREEN


def ensure_csv_file() -> None:
    if not CSV_FILE.exists():
        with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(CSV_HEADER)
        print(color("📄 File CSV creato: kitchen_sync_foods.csv", GREEN))


def read_food_items() -> list[dict]:
    if not CSV_FILE.exists():
        return []

    items = []
    with CSV_FILE.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            if not row or not row.get("nome_prodotto"):
                continue
            items.append(
                {
                    "nome_prodotto": row["nome_prodotto"].strip(),
                    "barcode": row["barcode"].strip(),
                    "expiry": row["expiry"].strip(),
                }
            )
    return items


def write_food_items(items: list[dict]) -> None:
    with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(CSV_HEADER)
        for item in items:
            writer.writerow([
                item["nome_prodotto"],
                item["barcode"],
                item["expiry"],
            ])
