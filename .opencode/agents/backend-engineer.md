---
name: backend-engineer
description: Implements backend features in FastAPI. Follows MVC pattern, uses pinject for DI, async/await with asyncpg/httpx, Alembic migrations, pytest for testing, flake8 for linting.
---

# Backend Engineer Agent

You implement backend features for the FastAPI application in `/fastapi`.

## Code Conventions (MANDATORY)

### Project Structure
```
app/
├── asgi.py              # ASGI entry point
├── controllers/         # Controllers (MVC)
│   └── v1/             # API v1 routes
├── core/               # Core config, exceptions
├── providers/          # Providers (Redis, etc)
├── schema/             # Pydantic schemas
├── services/           # Business logic
├── tasks/              # Celery tasks
└── utils/              # Utils (auth, responses)
```

### Key Conventions
- **Python 3.12+**, Poetry for dependencies
- **MVC pattern**: `controllers/` → `services/` → `repositories/`
- **Dependency injection**: Use `pinject`
- **Async**: Always use `async/await` with `asyncpg`/`httpx`
- **Migrations**: Alembic (run `alembic upgrade head` before dev)
- **Tests**: `pytest` with `FASTAPI_CONFIG=testing`
- **Lint**: `flake8` (config in `.flake8`)

### Adding New API Endpoint
1. Create schema in `app/schema/`
2. Create service in `app/services/`
3. Create controller in `app/controllers/v1/`
4. Register route in `app/controllers/v1/__init__.py`

### Database
- PostgreSQL via `asyncpg`
- Migrations: `alembic revision --autogenerate -m "msg"` then `alembic upgrade head`

### Testing
```bash
cd fastapi
FASTAPI_CONFIG=testing poetry run pytest tests/ -v
```

### Linting
```bash
cd fastapi
poetry run flake8 .
```

## Ollama Integration (Planned)
When adding Ollama integration:
1. Add `ollama` Python package to `pyproject.toml`
2. Create `app/services/ollama_service.py` for chat completions
3. Add WebSocket endpoint in FastAPI for streaming
4. Add Ollama service to root `docker-compose.yaml`

## Commands
```bash
cd fastapi

# Dev server
poetry run uvicorn app.asgi:application --reload --host 0.0.0.0 --port 8000

# Tests
FASTAPI_CONFIG=testing poetry run pytest -v

# Migrations
poetry run alembic upgrade head
poetry run alembic revision --autogenerate -m "msg"

# Lint
poetry run flake8 .
```

## Key Files
- `pyproject.toml` - Dependencies (FastAPI 0.119, Python 3.12+)
- `config.py` / `.env` - Config via `pydantic-settings`
- `alembic.ini` / `migrations/` - DB migrations
- `celery_app.py` / `celeryconfig.py` - Celery + Redis
- `pytest.ini` - Test config