from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi_pagination import add_pagination

from app.api.v1.routes import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import engine
from app.middlewares.request_id import RequestIdMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(RequestIdMiddleware)
add_pagination(app)


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}


@app.get("/ready", tags=["Health"])
async def ready():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda c: None)
        return {"status": "ready"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not-ready", "reason": str(e)},
        )


Instrumentator().instrument(app).expose(app, endpoint="/metrics")
app.include_router(api_router, prefix=settings.api_v1_prefix)
