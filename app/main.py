from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import create_engine
from app.core.config import settings
from app.router import product_router
from app.utils.db import create_all_or_upgrade_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_engine(settings.DATABASE_URL)
    app.state.db = engine.connect()
    create_all_or_upgrade_db(engine)
    yield
    app.state.db.close()


app = FastAPI(
    title="vegetable-market",
    description="A vegetable market API",
    version="0.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
    # default_response_class=ORJSONResponse,
)


app.include_router(product_router.router)
