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