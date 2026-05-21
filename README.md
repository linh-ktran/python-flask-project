# Industrial Asset Manager API

A Flask REST API for managing industrial sites, their energy managers, and machine assets (compressors, chillers, etc.). Built as a portfolio project showcasing modern Flask patterns.

## What it does

Manages the relationship between:
- **Sites** — industrial locations with a maximum electrical power capacity
- **Managers** — people responsible for one or more sites
- **Assets** — machines on a site (compressor, chiller, furnace, rolling mill)

The main business rule: you can't add machines to a site if their combined power would exceed the site's capacity.

## Project structure

```
app/
├── __init__.py          # App factory
├── config.py            # Dev/test/prod configs
├── api/                 # Endpoints (Flask-Smorest blueprints)
│   ├── health.py
│   ├── managers.py
│   ├── sites.py
│   └── assets.py
└── models/
    ├── models.py        # SQLAlchemy models
    └── schemas.py       # Marshmallow validation schemas

tests/
├── conftest.py          # Fixtures (in-memory DB)
├── test_models.py       # Unit tests
├── test_users_manager.py
├── test_users_site.py
└── test_users_asset.py
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Populate with sample data
python build_database.py

# Run the server
flask run --debug
```

API docs are served at http://localhost:5000/swagger-ui once the server is up.

## Running tests

```bash
pytest
# or with coverage
pytest --cov=app --cov-report=term-missing
```

50 tests covering models, business rules, and all API endpoints. Uses an in-memory SQLite DB so tests are fast and isolated.

## Docker

```bash
docker compose up --build
```

## API overview

**Managers** — `/api/managers`
- `GET /` — list all
- `POST /` — create (with optional `site_ids` to link)
- `GET /<id>`, `PATCH /<id>`, `DELETE /<id>`

**Sites** — `/api/sites`
- `GET /` — list all (includes assets and power info)
- `POST /` — create (with optional `manager_ids`)
- `GET /<id>`, `PATCH /<id>`, `DELETE /<id>`

**Assets** — `/api/sites/<site_id>/assets`
- `GET /` — list assets for a site
- `POST /` — add machine (validates power limit + type)
- `GET /<id>`, `PATCH /<id>`, `DELETE /<id>`

## Quick example

```bash
# Create a site
curl -X POST http://localhost:5000/api/sites \
  -H "Content-Type: application/json" \
  -d '{"name": "Factory A", "address": "123 Industrial Rd", "max_power": 20000}'

# Add a machine — works fine
curl -X POST http://localhost:5000/api/sites/1/assets \
  -H "Content-Type: application/json" \
  -d '{"name": "Compressor-1", "asset_type": "COMPRESSOR", "nominal_power": 5000}'

# Try adding one that's too powerful — returns 422
curl -X POST http://localhost:5000/api/sites/1/assets \
  -H "Content-Type: application/json" \
  -d '{"name": "Big-Furnace", "asset_type": "FURNACE", "nominal_power": 25000}'
```

## Tech used

- Flask 3 + Flask-Smorest (auto OpenAPI docs)
- SQLAlchemy + Flask-Migrate
- Marshmallow for input validation
- Pytest
- Docker + Gunicorn for production
- Ruff for linting

## License

MIT
