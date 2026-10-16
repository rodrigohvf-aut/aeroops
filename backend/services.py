from .database import get_connection


def create_airport(airport):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO airports (ident, name, country, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            airport.ident,
            airport.name,
            airport.country,
            airport.latitude,
            airport.longitude,
        ),
    )

    connection.commit()
    airport_id = cursor.lastrowid
    connection.close()

    return {**airport.model_dump(), "id": airport_id}


def list_airports():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, ident, name, country, latitude, longitude
        FROM airports
        ORDER BY name
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]