from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routes import auth, health, items, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Sample API",
    description="Minimal FastAPI service for API testing framework demonstration",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
