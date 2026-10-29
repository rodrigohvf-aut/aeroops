import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

import httpx


URL = "http://127.0.0.1:8000/airports"
REQUESTS = int(os.getenv("LOAD_REQUESTS", "100"))
WORKERS = int(os.getenv("LOAD_WORKERS", "10"))


def make_request(client):
    start = perf_counter()

    try:
        response = client.get(URL)
        success = response.status_code == 200
        error = None if success else f"HTTP {response.status_code}"
    except Exception as exception:
        success = False
        error = f"{type(exception).__name__}: {exception}"

    return success, perf_counter() - start, error


def main():
    start = perf_counter()

    limits = httpx.Limits(
        max_connections=WORKERS,
        max_keepalive_connections=WORKERS,
    )

    with httpx.Client(timeout=5.0, limits=limits, trust_env=False) as client:
        with ThreadPoolExecutor(max_workers=WORKERS) as executor:
            results = list(
                executor.map(lambda _: make_request(client), range(REQUESTS))
            )

    elapsed = perf_counter() - start
    successes = sum(success for success, _, _ in results)
    durations = sorted(
        duration for success, duration, _ in results if success
    )
    failures = Counter(
        error for success, _, error in results if not success
    )

    print(f"Requests: {REQUESTS}")
    print(f"Workers: {WORKERS}")
    print(f"Successful: {successes}")
    print(f"Failed: {REQUESTS - successes}")
    print(f"Total time: {elapsed:.2f} seconds")

    if durations:
        p95_index = int(0.95 * (len(durations) - 1))
        print(f"95th percentile successful response time: {durations[p95_index]:.3f} seconds")

    print(f"Failure types: {dict(failures)}")


if __name__ == "__main__":
    main()