# AeroOps

**Aviation Data Platform | Backend Engineering & Software Architecture**

AeroOps is a web-based aviation data platform designed to centralize, manage, and eventually analyze publicly available aviation information.

The project explores the design and development of a complete software solution, covering backend architecture, REST APIs, database integration, frontend development, automated testing, containerization, and infrastructure.

### Project Objectives

- Build a modular and maintainable aviation data platform.
- Design REST APIs using Python and FastAPI.
- Implement data persistence with SQLite and PostgreSQL.
- Integrate frontend, backend, and database components.
- Apply automated testing and API validation.
- Explore containerization, observability, and deployment practices.
- Evaluate architectural decisions, technical trade-offs, and scalability requirements.

### Current Development Stage

**Status: Active Development — Functional MVP**

The current version supports airport registration, listing, and deletion through a FastAPI backend and a browser-based interface.

The project also includes database integration, automated tests, API documentation, health checks, and Docker Compose configuration.

Future development will focus on aviation data integration, analytical dashboards, infrastructure deployment, and additional architectural improvements.

![AeroOps technical overview](docs/aeroops-overview.jpg)

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

```text
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
```

## Goal

Build a web dashboard for consulting, visualizing, and analyzing public aviation data worldwide without requiring paid data APIs.

The planned capabilities include airport and runway information, aircraft data imports, historical positions and trajectories, maps, charts, indicators by country and airport, and periodic data updates.

## Current architecture

AeroOps uses a containerized architecture with Nginx as a reverse proxy, FastAPI as the backend application, and PostgreSQL hosted on Supabase as the configured primary database.

```text
Browser
   |
   v
Nginx (localhost:8080)
   |
   v
FastAPI (Docker container, port 8000)
   |
   v
Supabase PostgreSQL
```

### Database configuration

The application supports different database configurations:

- **Supabase PostgreSQL:** Primary database when `DATABASE_URL` is configured.
- **SQLite:** Local fallback database when `DATABASE_URL` is not provided.
- **Local PostgreSQL:** Separate Docker service (`aeroops_test`) intended for database testing.

Database configuration is managed through environment variables, allowing the application to switch between local development and PostgreSQL environments without changing the application code.

### Infrastructure components

- **Nginx:** Reverse proxy that forwards HTTP requests to the FastAPI backend.
- **FastAPI:** Handles API requests, data validation, and application operations.
- **Supabase:** Hosts the remote PostgreSQL database.
- **Docker Compose:** Defines and manages the application containers and local database service.
- **Docker volumes:** Provide persistent storage for SQLite and the local PostgreSQL service.

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