from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
from urllib.request import urlopen
import os
from collections import Counter

URL = "http://127.0.0.1:8000/airports"
REQUESTS = int(os.getenv("LOAD_REQUESTS", "100"))
WORKERS = int(os.getenv("LOAD_WORKERS", "10"))


def make_request(_):
    start = perf_counter()

    try:
        with urlopen(URL, timeout=5) as response:
            success = response.status == 200
            error = None if success else f"HTTP {response.status}"
    except Exception as exception:
        success = False
        reason = getattr(exception, "reason", exception)
        error = f"{type(exception).__name__}: {reason}"

    return success, perf_counter() - start, error


def main():
    start = perf_counter()

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        results = list(executor.map(make_request, range(REQUESTS)))

    elapsed = perf_counter() - start
    successes = sum(success for success, _, _ in results)
    failure_types = Counter(
        error for success, _, error in results if not success
    )
    successful_durations = sorted(
        duration for success, duration, _ in results if success
    )

    print(f"Requests: {REQUESTS}")
    print(f"Successful: {successes}")
    print(f"Failed: {REQUESTS - successes}")
    print(f"Total time: {elapsed:.2f} seconds")

    if successful_durations:
        p95_index = int(0.95 * (len(successful_durations) - 1))
        print(
            "95th percentile successful response time: "
            f"{successful_durations[p95_index]:.3f} seconds"
        )

    print(f"Failure types: {dict(failure_types)}")

if __name__ == "__main__":
    main()