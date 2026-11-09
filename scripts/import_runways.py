import csv
from pathlib import Path

from backend.config import DATABASE_URL
from backend.database import get_connection


CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "runways.csv"


def optional_int(value):
    value = value.strip()
    return int(value) if value else None


def main():
    if DATABASE_URL:
        raise SystemExit("This import is for local SQLite only.")

    connection = get_connection()

    try:
        airport_codes = {
            row["ident"]
            for row in connection.execute("SELECT ident FROM airports")
        }

        imported = 0

        with CSV_PATH.open(encoding="utf-8-sig", newline="") as csv_file:
            for runway in csv.DictReader(csv_file):
                airport_ident = runway["airport_ident"].strip()

                if airport_ident not in airport_codes:
                    continue

                try:
                    values = (
                        int(runway["id"]),
                        airport_ident,
                        runway["le_ident"].strip() or None,
                        runway["he_ident"].strip() or None,
                        optional_int(runway["length_ft"]),
                        optional_int(runway["width_ft"]),
                        runway["surface"].strip() or None,
                        optional_int(runway["lighted"]),
                        optional_int(runway["closed"]),
                    )
                except ValueError:
                    continue

                cursor = connection.execute(
                    """
                    INSERT OR IGNORE INTO runways (
                        id, airport_ident, le_ident, he_ident,
                        length_ft, width_ft, surface, lighted, closed
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    values,
                )
                imported += cursor.rowcount

        connection.commit()
        print(f"Imported {imported} runways into local SQLite.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()