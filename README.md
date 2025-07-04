# CIVIS - AI Policy Document Compliance Audit Checker Backend Application

This is the backend system for CIVIS AI Policy Document Analysis — built with FastAPI, SQLAlchemy, Alembic, and modern tooling using [`uv`](https://github.com/astral-sh/uv) for dependency management.

---

## Setup Instructions

### 1. Install Python and `uv`

Make sure Python 3.10+ is installed.

Install `uv` (package manager + virtualenv):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

### 2. Clone the Repository

```bash
git clone https://github.com/<your-org>/civis-backend-policy-analyser.git
cd civis-backend-policy-analyser
```

---

### 3. Bootstrap the Project

```bash
make setup
```

This will:
- Create `.venv`
- Install base + AI + test dependencies
- Lock dependencies
- Generate `requirements.txt`

---

## Run the FastAPI Server

```bash
make run
```

Visit:

- Swagger UI: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Testing & Linting

### Run Tests

```bash
make test
```

### Run Tests with Coverage

```bash
make cov
```

### Run Linter

```bash
make lint
```

### Auto-fix Formatting & Style Issues

```bash
make fix
```

---

## Database (Postgres via Docker) + Alembic

### Build & Start DB

```bash
make db-build
make db-up
```

### Run Alembic Migrations

1. Initialize alembic (first time only):

```bash
alembic init -t async src/civis_backend_policy_analyser/alembic
```

2. Create a revision:

```bash
alembic revision --autogenerate -m "Initial schema"
```

3. Apply migration:

```bash
alembic upgrade head
```

### DB Utility Commands

```bash
make db-logs     # View logs
make db-psql     # Open psql shell
make db-down     # Stop and remove container
```

---

## Seed Initial Data

```bash
make seed
```

This runs `seed_data.py` inside the virtual environment.

---

## Project Structure

```
.
├── src/
│   └── civis_backend_policy_analyser/
│       ├── alembic/                  # Alembic migrations
│       ├── api/                      # FastAPI routes (entrypoints, routers)
│       ├── core/                     # App config, DB setup, constants
│       ├── model/                    # SQLAlchemy ORM models
│       ├── schemas/                  # Pydantic schemas (request/response)
│       ├── utils/                    # Helper functions, formatters, etc.
│       ├── views/                    # Route logic (e.g., CRUD handlers)
│       └── __init__.py
├── pyproject.toml                   # Dependency & build config
├── Makefile                         # Task automation
├── requirements.txt                 # (auto-generated by uv)
├── seed_data.py                     # DB seeding script
└── README.md                        # Project documentation

```

---

## Developer Notes

- `uv` manages dependencies via `pyproject.toml` with groups: `[project]`, `ai`, `test`.
- No manual activation of `.venv` is required when using `uv run`.
- Prefer `make` targets for consistent workflows.
- `make setup` is the fastest way to bootstrap everything from scratch.
- `make quick-start` is for the quick start with sample data in database if docker running in local.

---

## Quick Commands Reference

| Command           | Action                                 |
|------------------------|-----------------------------------------|
| `make quick-start`     | Start full application with sample data |
| `make setup`           | Full setup: venv + deps + lock + freeze |
| `make run`             | Start FastAPI app                       |
| `make lint`            | Run linter                              |
| `make fix`             | Auto-fix lint issues                    |
| `make test`            | Run unit tests                          |
| `make cov`             | Run tests with coverage                 |
| `make seed`            | Seed initial data                       |
| `make db-up`           | Start DB container                      |
| `make db-down`         | Stop DB container                       |
| `make db-psql`         | Open DB shell inside container          |

---

