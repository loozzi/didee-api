# Didee API - FastAPI REST API

A production-ready REST API application built with FastAPI, SQLAlchemy, and Alembic for database migrations.

## Project Structure

```
didee-api/
├── alembic/                    # Database migrations
│   ├── versions/              # Migration files
│   ├── env.py                 # Alembic environment configuration
│   └── script.py.mako         # Migration template
├── app/
│   ├── main.py                # FastAPI application entry point
│   ├── api/
│   │   └── v1/
│   │       └── api.py         # API router aggregator
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   ├── security.py        # Security utilities (JWT, password hashing)
│   │   ├── schemas.py         # Common response schemas
│   │   ├── exceptions.py      # Exception handlers
│   │   ├── middleware.py      # Custom middleware
│   │   ├── logging_config.py  # Logging configuration
│   │   └── decorators/
│   │       └── response.py    # Response decorator
│   ├── db/
│   │   ├── base.py            # Import all models for Alembic
│   │   └── session.py         # Database session and Base
│   ├── modules/
│   │   ├── auth/              # Authentication module
│   │   │   ├── router.py      # Auth endpoints
│   │   │   └── schemas.py     # Auth schemas
│   │   └── users/             # Users module
│   │       ├── router.py      # User endpoints
│   │       ├── schemas.py     # User schemas
│   │       ├── models.py      # User model
│   │       └── crud.py        # User CRUD operations
├── tests/
│   ├── conftest.py            # Test fixtures
│   ├── test_main.py           # Main endpoint tests
│   ├── test_auth.py           # Auth endpoint tests
│   └── test_users.py          # User endpoint tests
├── logs/                       # Application logs (gitignored)
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore file
├── alembic.ini                # Alembic configuration
├── pyproject.toml             # Project metadata and dependencies
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Features

- ✅ **FastAPI** - High-performance REST API framework
- ✅ **SQLAlchemy ORM** - Database operations with ORM
- ✅ **Alembic** - Database migration management
- ✅ **Pydantic v2** - Data validation and settings management
- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **Password Hashing** - Argon2 password hashing
- ✅ **Modular Architecture** - Organized by modules (users, auth, etc.)
- ✅ **PostgreSQL** - Production database support (SQLite for dev)
- ✅ **CORS Middleware** - Cross-origin resource sharing
- ✅ **Request Logging** - Automatic request/response logging
- ✅ **Exception Handling** - Global exception handlers
- ✅ **Environment-based Config** - Support for dev/staging/prod
- ✅ **Health Check** - Database connectivity check
- ✅ **Comprehensive Testing** - Pytest with fixtures
- ✅ **Type Hints** - Full type annotation support

## Setup

### 1. Install uv

If you don't have `uv` installed, install it first:

**Windows:**

```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/Mac:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install dependencies

```bash
uv sync
```

Or if you don't have a `pyproject.toml` yet:

```bash
uv pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and update the values:

```bash
copy .env.example .env
```

Edit `.env` with your database credentials and settings:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
```

### 4. Initialize the database

Create your database, then run Alembic migrations:

```bash
# Create initial migration
uv run alembic revision --autogenerate -m "Initial migration"

# Apply migrations
uv run alembic upgrade head
```

### 5. Run the application

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

- API Root: http://localhost:8000
- Interactive docs (Swagger): http://localhost:8000/api/v1/docs
- Alternative docs (ReDoc): http://localhost:8000/api/v1/redoc
- Health check: http://localhost:8000/health

## Database Migrations

### Create a new migration

```bash
uv run alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
uv run alembic upgrade head
```

### Rollback migration

```bash
uv run alembic downgrade -1
```

### View migration history

```bash
uv run alembic history
```

## API Endpoints

### Health & Info

- `GET /` - API information and links
- `GET /health` - Health check with database status

### Authentication (`/api/v1/auth`)

- `POST /api/v1/auth/login` - Login and get access token
- `POST /api/v1/auth/token` - OAuth2 compatible token endpoint (for Swagger)
- `GET /api/v1/auth/me` - Get current user profile (requires authentication)

### Users (`/api/v1/users`)

- `GET /api/v1/users/` - List all users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Example Usage

1. **Create a user:**

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"testuser","password":"securepass123"}'
```

2. **Login:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"securepass123"}'
```

3. **Access protected endpoint:**

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Testing

Run tests with pytest:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=app tests/
```

## Adding New Features

### 1. Create a new model

Create a new file in `app/models/`:

```python
# app/models/item.py
from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
```

### 2. Import the model in base.py

```python
# app/db/base.py
from app.models.item import Item  # noqa
```

### 3. Create schemas

```python
# app/schemas/item.py
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True
```

### 4. Create CRUD operations

```python
# app/crud/item.py
from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate

def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

### 5. Create endpoints

```python
# app/api/v1/endpoints/items.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.item import Item, ItemCreate
from app.crud import item as crud_item

router = APIRouter()

@router.post("/", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return crud_item.create_item(db=db, item=item)
```

### 6. Register the router

```python
# app/api/v1/api.py
from app.api.v1.endpoints import items

api_router.include_router(items.router, prefix="/items", tags=["items"])
```

### 7. Create and apply migration

```bash
uv run alembic revision --autogenerate -m "Add items table"
uv run alembic upgrade head
```

## Environment Variables

| Variable                    | Description                 | Default             | Required |
| --------------------------- | --------------------------- | ------------------- | -------- |
| ENVIRONMENT                 | Environment mode            | development         | No       |
| DATABASE_URL                | Database connection string  | sqlite:///./app.db  | Yes      |
| PROJECT_NAME                | Application name            | FastAPI Application | No       |
| VERSION                     | API version                 | 1.0.0               | No       |
| API_V1_PREFIX               | API v1 prefix               | /api/v1             | No       |
| SECRET_KEY                  | JWT secret key              | (must change)       | Yes      |
| ALGORITHM                   | JWT algorithm               | HS256               | No       |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration (minutes)  | 30                  | No       |
| BACKEND_CORS_ORIGINS        | Allowed CORS origins (JSON) | []                  | No       |

**Note:** In production, `SECRET_KEY` must be changed from the default value!

## Technologies

- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type hints
- **PostgreSQL** - Primary database
- **uv** - Fast Python package installer and resolver
- **Uvicorn** - ASGI server
- **Pytest** - Testing framework
- **Python-Jose** - JWT implementation
- **Passlib** - Password hashing library

## License

MIT
