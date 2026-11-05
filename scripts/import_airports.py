import csv
from pathlib import Path

from backend.config import DATABASE_URL
from backend.database import get_connection


CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "airports.csv"
MAX_AIRPORTS = 80


def main():
    if DATABASE_URL:
        raise SystemExit("This first import is for local SQLite only.")

    connection = get_connection()

    try:
        existing = connection.execute(
            "SELECT ident, country FROM airports"
        ).fetchall()

        known_codes = {row["ident"] for row in existing}
        known_countries = {row["country"] for row in existing}
        sample_countries = {
            country for country in known_countries
            if len(country) == 2 and country.isupper()
        }
        remaining = max(0, MAX_AIRPORTS - len(sample_countries))
        imported = 0

        if remaining == 0:
            print("The airport sample is already at its limit.")
            return

        with CSV_PATH.open(encoding="utf-8-sig", newline="") as csv_file:
            for airport in csv.DictReader(csv_file):
                if airport["type"] != "large_airport":
                    continue

                code = airport["icao_code"].strip()
                country = airport["iso_country"].strip()

                if (
                    len(code) != 4
                    or not code.isalnum()
                    or not country
                    or code in known_codes
                    or country in known_countries
                ):
                    continue

                try:
                    latitude = float(airport["latitude_deg"])
                    longitude = float(airport["longitude_deg"])
                except ValueError:
                    continue

                if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                    continue

                connection.execute(
                    """
                    INSERT INTO airports
                        (ident, name, country, latitude, longitude)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (code, airport["name"], country, latitude, longitude),
                )

                known_codes.add(code)
                known_countries.add(country)
                imported += 1

                if imported >= remaining:
                    break

        connection.commit()
        print(f"Imported {imported} airports into local SQLite.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()