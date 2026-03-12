# Verkko Inventory Service

A product inventory management microservice built with FastAPI, SQLAlchemy, and PostgreSQL, following Domain-Driven Design (DDD) and Clean Architecture principles.

## Architecture Overview

The project is organized as a modular monolith, where each module is self-contained and follows a layered architecture. The layers enforce a strict dependency rule: inner layers never depend on outer layers.

```
src/
├── common/                  # Shared building blocks (abstracts, DTOs, filters, interceptors)
├── modules/
│   ├── inventory_record/    # Core business module
│   │   ├── domain/          # Enterprise business rules
│   │   ├── application/     # Use cases, ports, facades
│   │   ├── infrastructure/  # Database adapters, ORM entities
│   │   └── presentation/    # Controllers, request/response DTOs
│   └── shared/              # Cross-cutting modules (config, database, health)
├── container.py             # Root dependency injection container
├── routes.py                # Route registration
├── app.py                   # Application bootstrap
└── main.py                  # Entry point
```

### Domain Layer

The innermost layer contains the core business rules. The `InventoryRecord` entity encapsulates validation logic (non-empty product ID, non-negative quantity, required timestamp) and is completely independent of frameworks and infrastructure.

### Application Layer

Orchestrates business operations through the **CQRS pattern** (Command Query Responsibility Segregation):

- **Commands** — `CreateInventoryRecordsCommand` carries write intent with its data.
- **Queries** — `SearchInventoryRecordQuery` carries read intent with filter/pagination parameters.
- **Use Cases** — Each operation is a dedicated class (`CreateInventoryRecordsUseCase`, `SearchInventoryRecordUseCase`) extending `BaseUseCase`, responsible for a single action.
- **Mappers** — Transform domain entities into result types, keeping mapping logic isolated.
- **Ports** — `InventoryRepository` is an abstract interface that the domain defines and the infrastructure implements (Dependency Inversion).
- **Facade** — `InventoryRecordFacade` is an abstract contract that the presentation layer depends on. `InventoryRecordApplicationService` implements it and delegates to the appropriate use case.

### Infrastructure Layer

Implements the ports defined by the application layer:

- **SQLAlchemy ORM Entity** — `InventoryRecordSqlAlchemy` maps to the `inventory_records` table with indexed columns (`product_id`, `timestamp`) for query performance.
- **Repository** — `SqlAlchemyInventoryRepository` implements `InventoryRepository`, handling all database operations including pagination with separate `COUNT` and `SELECT` queries.

### Presentation Layer

Handles HTTP concerns and is the only layer aware of FastAPI:

- **Controllers** — `InventoryRecordController` registers routes and translates HTTP requests into application commands/queries. Uses Pydantic's `model_validate` (equivalent to NestJS `plainToInstance`) for automatic result-to-DTO mapping.
- **DTOs** — Separate request and response DTOs with Pydantic validation. `InventoryRecordResponseDto` uses `validation_alias` to map internal `product_id` to the API's `productid` convention.
- **Response Standardization** — `PresentationResponseHandler` (a custom `APIRoute` subclass, analogous to a NestJS interceptor) wraps all controller responses in a consistent `PresentationResponse` envelope (`success`, `data`, `message`, `error`, `timestamp`).

## Design Patterns

### Dependency Injection

The project uses `dependency-injector` for IoC. Each module has its own `DeclarativeContainer` that wires up repositories, use cases, services, and controllers. The root `Container` composes module containers together.

### Facade Pattern

The application layer exposes an abstract `InventoryRecordFacade` as its public API. The presentation layer depends only on this contract — it never directly references use cases or repositories. This decouples layers and makes the application service the single entry point for all module operations.

### Port-Adapter Pattern (Hexagonal Architecture)

Domain and application layers define abstract ports (`InventoryRepository`, `PersistencePort`). Infrastructure provides concrete adapters (`SqlAlchemyInventoryRepository`, `SqlAlchemyAdapter`). Swapping databases or ORMs requires only a new adapter — no changes to business logic.

### CQRS

Commands and queries are separated into distinct types and use cases. This makes the codebase easier to reason about, test, and scale independently (read-heavy vs write-heavy paths could be optimized separately).

### Exception Filter

`ExceptionFilter` centralizes all error handling in one class, registered on the FastAPI app. It handles:
- **Domain/Application errors** (`AppException`) — mapped to appropriate HTTP status codes.
- **Validation errors** (`RequestValidationError`) — returned as 400 with field-level messages.
- **Unhandled exceptions** — returned as 500 with a generic message (no internal details leaked), logged server-side.

### Secret Management

The service integrates with HashiCorp Vault for dynamic database credentials. Vault issues short-lived credentials with automatic rotation via a subscribe/callback mechanism, eliminating static passwords from configuration.

## Setup Instructions

### Prerequisites

- Python 3.12+
- Docker and Docker Compose

### Running with Docker (Recommended)

1. Start infrastructure (PostgreSQL + Vault):

```bash
cd deploy
docker compose -f docker-compose.infra.dev.yml up -d
```

2. Start the application:

```bash
docker compose -f docker-compose.dev.yml up -d
```

The service will be available at `http://localhost:8001`.

### Running Locally

1. Start infrastructure:

```bash
cd deploy
docker compose -f docker-compose.infra.dev.yml up -d
```

2. Copy and configure environment variables:

```bash
cp .env.example .env
```

Add the following to your `.env`:

```
VAULT_ADDR=http://localhost:8201
VAULT_TOKEN=dev-root-token
DB_HOST=localhost
DB_PORT=5433
DB_NAME=verkko_db
DB_SSL=true
DB_SYNC=true
```

3. Install dependencies and run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn src.main:app --reload
```

The service will be available at `http://localhost:8000`.

## API Documentation

All responses are wrapped in a standard envelope:

```json
{
  "success": true,
  "data": { ... },
  "message": null,
  "error": null,
  "timestamp": "2026-03-12T15:00:00+00:00"
}
```

### POST /inventory/update

Create inventory records.

**Request:**

```bash
curl -X POST http://localhost:8000/inventory/update \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"productid": "SKU12345", "quantity": 100, "timestamp": "2026-03-04T10:30:00Z"},
      {"productid": "SKU67890", "quantity": 50, "timestamp": "2026-03-04T12:00:00Z"}
    ]
  }'
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "records": [
      {"id": 1, "productid": "SKU12345", "quantity": 100, "timestamp": "2026-03-04T10:30:00Z"},
      {"id": 2, "productid": "SKU67890", "quantity": 50, "timestamp": "2026-03-04T12:00:00Z"}
    ],
    "count": 2
  }
}
```

### GET /inventory/query

Search inventory records with filtering and pagination.

| Parameter        | Type   | Required | Description                          |
|------------------|--------|----------|--------------------------------------|
| `productid`      | string | Yes      | Filter by product ID                 |
| `starttimestamp`  | string | No       | ISO 8601, filter from this time      |
| `endtimestamp`    | string | No       | ISO 8601, filter up to this time     |
| `limit`          | int    | No       | Page size (1-100, default: 20)       |
| `offset`         | int    | No       | Skip N records (default: 0)          |

**Request:**

```bash
curl "http://localhost:8000/inventory/query?productid=SKU12345&starttimestamp=2026-03-04T00:00:00Z&endtimestamp=2026-03-05T00:00:00Z&limit=10&offset=0"
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "items": [
      {"id": 1, "productid": "SKU12345", "quantity": 100, "timestamp": "2026-03-04T10:30:00Z"}
    ],
    "total": 1
  }
}
```

### Error Responses

**Validation Error (400):**

```json
{
  "success": false,
  "error": "VALIDATION_ERROR",
  "message": "body -> items -> 0 -> productid: String should have at least 1 character"
}
```

**Internal Server Error (500):**

```json
{
  "success": false,
  "error": "INTERNAL_SERVER_ERROR",
  "message": "An unexpected error occurred."
}
```

## Design Decisions & Trade-offs

### Why FastAPI?

FastAPI provides async support out of the box, automatic OpenAPI documentation, and native Pydantic integration for request validation — making it ideal for building high-performance APIs with minimal boilerplate.

### Why SQLAlchemy?

SQLAlchemy is the most mature Python ORM with excellent async support via `asyncpg`. Its declarative mapping and query builder allow clean separation between domain entities and persistence entities, which is essential for DDD.

### Why DDD and Clean Architecture?

While the scope of this task is small, the architecture demonstrates how the service would scale in a real system. Each layer has a clear responsibility, dependencies point inward, and swapping infrastructure (e.g., switching from PostgreSQL to another store) requires no changes to business logic. The trade-off is more files and indirection for a simple CRUD service, but this pays off as complexity grows.

### Why CQRS?

Separating commands from queries makes each operation explicit and independently testable. In a production system, this separation enables different optimization strategies for reads vs writes (e.g., read replicas, caching, event sourcing).

### Why Vault for Secrets?

Static database credentials in environment variables are a security risk. Vault provides dynamic, short-lived credentials with automatic rotation. The service subscribes to credential changes and transparently reconnects — zero-downtime rotation.

### What Would Be Different in Production?

- **Idempotency** — Ensure duplicate requests don't create duplicate records (via unique constraints, an idempotency table, or request-level caching depending on domain rules).
- **Testing** — Comprehensive unit tests for domain logic, integration tests with a real database, and contract tests for the API.
- **Observability** — Structured logging, distributed tracing (OpenTelemetry), and metrics (Prometheus).
- **Rate Limiting** — Protect the ingestion endpoint from abuse.
- **CI/CD** — Automated linting, testing, building, and deployment pipeline.
- **Database Migrations** — Alembic for versioned schema migrations instead of auto-sync.
