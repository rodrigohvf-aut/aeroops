# AeroOps

![AeroOps technical overview](docs/aeroops-overview.jpg)

AeroOps is an educational platform for exploring and analyzing global aviation data. The project is being developed step by step, starting locally and preparing for deployment on a VPS and possible expansion to AWS.

## Current status

The current application includes:

- A FastAPI backend for listing, creating, and deleting airports.
- A web interface built with HTML, CSS, and JavaScript.
- Data validation through the API's airport model.
- SQLite for local development.
- A PostgreSQL development database on Supabase.
- A separate PostgreSQL test database in local Docker.
- A versioned SQL migration for the `airports` table.
- Automated tests with pytest and Playwright.
- OpenAPI documentation at `/docs`, `/redoc`, and `/openapi.json`.
- API and database health endpoints, request logs, and basic measurements.
- Docker Compose services for the API, Nginx, and local PostgreSQL.

The Docker Compose API is connected to Supabase PostgreSQL; listing, creating, and deleting airports were verified. The separate local PostgreSQL database `aeroops_test` was used in a manual run of eight non-browser tests. The default local test run and browser E2E test use SQLite.

## Project structure

aeroops/
├── backend/                              FastAPI application
│   ├── __init__.py                       Marks backend as a Python package
│   ├── main.py                           Creates the app, middleware and health routes
│   ├── routes.py                         Airport API endpoints
│   ├── models.py                         Airport data validation
│   ├── services.py                       Airport operations and database queries
│   ├── database.py                       SQLite or PostgreSQL connection
│   └── config.py                         Settings read from environment variables
│
├── frontend/                             Browser interface
│   ├── index.html                        Dashboard structure and forms
│   ├── style.css                         Colours and layout
│   └── app.js                            API calls and dashboard interactions
│
├── tests/                                Automated tests
│   ├── test_api.py                        API behaviour
│   ├── test_models.py                     Data validation
│   ├── test_contract.py                   OpenAPI route contract
│   ├── test_regression.py                 Existing routes
│   └── test_e2e.py                        Real-browser workflow
│
├── scripts/                              Manual performance tools
│   ├── load_test.py                       Request load test
│   └── load_test_pooled.py                Load test with reused connections
│
├── supabase/                             Supabase configuration
│   ├── config.toml                        Local Supabase project settings
│   └── migrations/
│       └── 20261023000000_create_airports.sql
│                                         PostgreSQL airports table migration
│
├── nginx/
│   └── nginx.conf                         Reverse proxy configuration
├── docs/
│   ├── aeroops-overview.jpg               Architecture infographic
│   └── load-test-results.md               Recorded performance results
├── data/                                  Folder reserved for project data
│
├── Dockerfile                             Instructions to build the API image
├── docker-compose.yml                     Runs the local containers together
├── requirements.txt                       Python dependencies
├── .env.example                           Example environment settings
├── .env                                   Local settings and credentials
├── .gitignore                             Files Git should ignore
├── aeroops.db                             Local SQLite database
├── aeroops.code-workspace                 VS Code workspace settings
├── README.md                              Project overview
│
├── .venv/                                 Local Python environment
├── .vscode/                               Local VS Code settings
└── .git/                                  Git history and repository settings


## Goal

Build a web dashboard for consulting, visualizing, and analyzing public aviation data worldwide without requiring paid data APIs.

The planned capabilities include airport and runway information, aircraft data imports, historical positions and trajectories, maps, charts, indicators by country and airport, and periodic data updates.

## Current architecture

```text
Browser
├── Frontend served locally on port 5500
└── Nginx on localhost:8080
    └── FastAPI on port 8000
        └── SQLite in a persistent Docker volume
```
The backend can also connect to Supabase PostgreSQL when DATABASE_URL is set in its environment. Without DATABASE_URL, it uses SQLite.

## API

- GET / — confirms that the API is running.
- GET /health — checks the API.
- GET /health/database — checks the database connection.
- GET /airports — lists airports.
- POST /airports — creates an airport.
- DELETE /airports/{airport_id} — deletes an airport.

## Data sources to evaluate

- OurAirports.
- OpenSky Network, within its free-use limits.
- Open-Meteo.
- Other public sources compatible with the project.
These sources are part of the plan; they have not yet been integrated.

## Product indicators

- Total airports stored.
- Airport list requests.
- Airports created and deleted.
- Validation errors.
- Dashboard visits.
- Countries represented.
- Date of the latest data update.
These indicators describe the product measurement plan. Their implementation and reporting will evolve with the application.

## Planned infrastructure

- A production database separate from development and testing.
- Deployment on a Hostinger VPS with Ubuntu and Docker Compose.
- A public domain, DNS, HTTPS, and firewall rules.
- External backups, monitoring, and recovery procedures.
- Possible migration to AWS as the project grows.

## Scope and limitations

AeroOps is an educational and analytical project. It is not an aircraft control system, a certified aviation safety system, or a substitute for official flight information. Its data must not be used as the sole basis for real-world flight, navigation, or operational safety decisions.

Real-time aircraft tracking and paid data APIs are not requirements for the initial version. Apart from the planned VPS, the project aims to use free software and data sources.