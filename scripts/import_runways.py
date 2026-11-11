import csv
from pathlib import Path

from backend.config import DATABASE_URL
from backend.database import get_connection


CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "runways.csv"


def optional_int(value):
    value = value.strip()
    return int(value) if value else None


def optional_coordinate(value, minimum, maximum):
    value = value.strip()

    if not value:
        return None

    coordinate = float(value)

    if not minimum <= coordinate <= maximum:
        raise ValueError("Invalid coordinate")

    return coordinate


def main():
    connection = get_connection()

    placeholder = "%s" if DATABASE_URL else "?"
    placeholders = ", ".join([placeholder] * 13)

    upsert_sql = f"""
        INSERT INTO runways (
            id, airport_ident, le_ident, he_ident,
            length_ft, width_ft, surface, lighted, closed,
            le_latitude_deg, le_longitude_deg,
            he_latitude_deg, he_longitude_deg
        )
        VALUES ({placeholders})
        ON CONFLICT (id) DO UPDATE SET
            le_latitude_deg = excluded.le_latitude_deg,
            le_longitude_deg = excluded.le_longitude_deg,
            he_latitude_deg = excluded.he_latitude_deg,
            he_longitude_deg = excluded.he_longitude_deg
    """

    try:
        airport_codes = {
            row["ident"]
            for row in connection.execute("SELECT ident FROM airports")
        }

        processed = 0

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
                        optional_coordinate(
                            runway["le_latitude_deg"], -90, 90
                        ),
                        optional_coordinate(
                            runway["le_longitude_deg"], -180, 180
                        ),
                        optional_coordinate(
                            runway["he_latitude_deg"], -90, 90
                        ),
                        optional_coordinate(
                            runway["he_longitude_deg"], -180, 180
                        ),
                    )
                except ValueError:
                    continue

                connection.execute(upsert_sql, values)
                processed += 1

        connection.commit()

        database_name = "PostgreSQL" if DATABASE_URL else "local SQLite"
        print(f"Processed {processed} runways in {database_name}.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()