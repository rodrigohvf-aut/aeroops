# Local load test results

## 2026-10-29 — Baseline

- Target: local API, `GET /airports`, SQLite
- Command: `python scripts/load_test.py`
- Requests: 100
- Concurrent workers: 10
- Successful: 100
- Failed: 0
- Total time: 1.13 seconds
- 95th percentile response time: 0.701 seconds

This is a local baseline. It does not represent the maximum capacity of the application.

## 2026-10-29 — Connection pressure

Target: local API, `GET /airports`, SQLite. Client and API ran on the same computer. Each request had a 5-second timeout.

| Requests | Workers | Successful | Failed | Total time | Successful response p95 |
|---:|---:|---:|---:|---:|---:|
| 10,000 | 200 | 10,000 | 0 | 32.65 s | 0.903 s |
| 10,000 | 250 | 9,996 | 4 | 34.67 s | 1.933 s |
| 10,000 | 250 | 9,973 | 27 | 35.96 s | 1.799 s |
| 10,000 | 300 | 9,837 | 163 | 31.62 s | 2.214 s |

All recorded failures were connection refusals (`WinError 10061`).
In these local runs, refusals appeared at 250 and 300 workers, but not at 200 workers.
This does not establish the API's independent or production capacity.

## 2026-10-29 — Repeated runs after limiting response-time history

Local API with SQLite; 10,000 GET /airports requests and 200 client workers per run. The same API process was used for all three runs.

| Run | Failed | Total time | Successful response p95 | API memory after run |
|---:|---:|---:|---:|---:|
| 1 | 0 | 38.75 s | 1.673 s | 74.6 MB |
| 2 | 0 | 63.61 s | 2.202 s | 78.9 MB |
| 3 | 0 | 47.40 s | 1.894 s | 78.7 MB |

API memory before the first run was 57.6 MB. It remained near 79 MB after the second and third runs. This short observation does not establish long-term memory behavior or explain earlier connection failures.

## 2026-10-29 — Per-request logging comparison

Local API with SQLite; 10,000 GET /airports requests and 250 client workers per run. For these two runs, Uvicorn access logs and the application's per-request INFO logs were disabled temporarily.

| Run | Successful | Failed | Total time | Successful response p95 |
|---:|---:|---:|---:|---:|
| 1 | 10,000 | 0 | 29.47 s | 1.716 s |
| 2 | 9,991 | 9 | 25.94 s | 1.783 s |

The 9 failures in the second run were connection refusals (`WinError 10061`). Disabling per-request logs did not eliminate connection refusals. These local runs do not establish whether the client, operating system, or API was the limiting component.

## 2026-10-29 — Reused HTTP connections

The local API was tested with `scripts/load_test_pooled.py`, using a shared HTTPX client to reuse connections. Client and API ran on the same computer.

- Target: `GET /airports` with SQLite
- Requests: 10,000
- Client workers: 250
- Successful: 9,887
- Failed: 113
- Total time: 120.99 seconds
- Successful response p95: 7.555 seconds
- Failure type: `ReadTimeout`

Connection reuse did not eliminate failures in this run. The earlier script produced connection refusals; this run produced read timeouts. These results do not isolate whether the limiting factor was the API, the test client, or their shared computer.