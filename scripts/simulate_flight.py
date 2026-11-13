import json
import time
from datetime import datetime, timezone
from urllib.request import Request, urlopen


API_URL = "http://127.0.0.1:8000/aircraft/positions"

# Cinco pontos fictícios próximos ao aeroporto de Guarulhos.
POINTS = [
    (-23.4356, -46.4731),
    (-23.4200, -46.4300),
    (-23.4000, -46.3800),
    (-23.3800, -46.3300),
    (-23.3500, -46.2800),
]


def main():
    for latitude, longitude in POINTS:
        position = {
            "icao24": "abc124",
            "latitude": latitude,
            "longitude": longitude,
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "source": "simulated",
        }

        request = Request(
            API_URL,
            data=json.dumps(position).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=10) as response:
            if response.status != 201:
                raise RuntimeError(f"Unexpected status: {response.status}")

        print(f"Sent simulated position: {latitude}, {longitude}")
        time.sleep(5)


if __name__ == "__main__":
    main()