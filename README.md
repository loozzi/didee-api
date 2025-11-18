# FastAPI + Alembic REST API Project

A production-ready REST API application built with FastAPI and Alembic for database migrations.

## Project Structure

```
be/
├── alembic/                    # Database migrations
│   ├── versions/              # Migration files
│   ├── env.py                 # Alembic environment configuration
│   └── script.py.mako         # Migration template
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/     # API endpoints
│   │       │   └── users.py   # User endpoints
│   │       └── api.py         # API router
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   └── security.py        # Security utilities (JWT, password hashing)
│   ├── crud/
│   │   └── user.py            # CRUD operations for users
│   ├── db/
│   │   ├── base.py            # Import all models for Alembic
│   │   └── session.py         # Database session and Base
│   ├── models/
│   │   └── user.py            # SQLAlchemy models
│   └── schemas/
│       └── user.py            # Pydantic schemas
├── tests/
│   ├── conftest.py            # Test fixtures
│   ├── test_main.py           # Main endpoint tests
│   └── test_users.py          # User endpoint tests
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore file
├── alembic.ini                # Alembic configuration
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Features

- ✅ FastAPI for high-performance REST API
- ✅ SQLAlchemy ORM for database operations
- ✅ Alembic for database migrations
- ✅ Pydantic for data validation
- ✅ JWT authentication utilities
- ✅ Password hashing with bcrypt
- ✅ CRUD operations example (Users)
- ✅ Structured project layout
- ✅ PostgreSQL support
- ✅ CORS middleware
- ✅ Environment-based configuration
- ✅ Pytest for testing

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
uv run uvicorn main:app --reload
```

The API will be available at:

- API: http://localhost:8000
- Interactive docs: http://localhost:8000/api/v1/docs
- Alternative docs: http://localhost:8000/api/v1/redoc

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

### Health Check

- `GET /` - Root endpoint
- `GET /health` - Health check

### Users (API v1)

- `GET /api/v1/users/` - List all users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

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

| Variable                    | Description                  | Default             |
| --------------------------- | ---------------------------- | ------------------- |
| DATABASE_URL                | PostgreSQL connection string | -                   |
| PROJECT_NAME                | Application name             | FastAPI Application |
| VERSION                     | API version                  | 1.0.0               |
| API_V1_PREFIX               | API v1 prefix                | /api/v1             |
| SECRET_KEY                  | JWT secret key               | -                   |
| ALGORITHM                   | JWT algorithm                | HS256               |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration time        | 30                  |
| BACKEND_CORS_ORIGINS        | Allowed CORS origins         | []                  |

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
