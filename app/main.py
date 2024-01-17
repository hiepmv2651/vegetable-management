from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from app.core.config import settings
from app.handler.exception_handlers import custom_http_exception_handler, validation_exception_handler
from app.router import category_router, product_router
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
app.include_router(category_router.router)

app.exception_handler(HTTPException)(custom_http_exception_handler)
app.exception_handler(RequestValidationError)(validation_exception_handler)

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")