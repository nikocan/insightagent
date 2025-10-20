"""Application entrypoint wiring routers, database, and startup hooks."""

from fastapi import FastAPI

from .database import get_db, initialize_db
from .routers import (
    adstudio,
    analytics,
    creatives,
    insights,
    keywords,
    offers,
    products,
    reports,
    reviews,
    rfqs,
    suppliers,
)
from .services.sample_data import seed_demo_data

# Create database tables on startup.
initialize_db()

app = FastAPI(title="InsightAgent API", version="0.1.0")

# Register API routers representing each product module.
app.include_router(analytics.router)
app.include_router(products.router)
app.include_router(insights.router)
app.include_router(keywords.router)
app.include_router(creatives.router)
app.include_router(adstudio.router)
app.include_router(offers.router)
app.include_router(suppliers.router)
app.include_router(reports.router)
app.include_router(reviews.router)
app.include_router(rfqs.router)


@app.on_event("startup")
async def startup_event() -> None:
    """Seed the database with representative demo content."""
    with get_db() as conn:
        seed_demo_data(conn)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    """Return service health metadata for monitoring purposes."""
    return {"status": "ok"}
