import time
import uvicorn as uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.responses import ORJSONResponse,Response
from fastapi import status
from starlette.middleware.cors import CORSMiddleware
from app.logging import init_logging, logger
from app.api.endpoints.api import api_router as api_router_v1
from app.exceptions import APIValidationError

from fastapi.exceptions import RequestValidationError, StarletteHTTPException
{%- if cookiecutter.enable_kafka == "True" %}
from app.utils.kafka_producer import start_kafka, shutdown_kafka

{%- endif %}

{%- if cookiecutter.enable_redis == "True" %}
from app.utils.redis_utils import shutdown_redis

{%- endif %}

{%- if cookiecutter.orm == "tortoise" %}
from app.db.init_db import get_db

{%- endif %}

{%- if cookiecutter.orm == "beanie" %}
from app.db.beanie import get_db

{%- endif %}

{%- if cookiecutter.orm == "mongo" %}
from app.db.mongodb_utils import connect_to_mongo, close_mongo_connection

{%- endif %}


from app.core.config import settings

{%- if cookiecutter.enable_sentry == "True" %}
import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    integrations=[
        StarletteIntegration(transaction_style="endpoint"),
        FastApiIntegration(transaction_style="endpoint"),
    ],
)
{%- endif %}

init_logging()
# Core Application Instance
app = FastAPI(
    debug=settings.DEBUG,
    default_response_class=ORJSONResponse,
    docs_url=settings.DOCS_URL if not settings.DEBUG else None,
    openapi_url=f"/api/{settings.API_V1_STR}/openapi.json",
    redoc_url=settings.REDOC_URL if not settings.DEBUG else None,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Unprocessable Entity (Validation Error)",
            "model": APIValidationError,  # This will add OpenAPI schema to the docs
        },
    },
)


@app.get("/health", tags=["health"])
def healthcheck():
    return {"message": "ok"}

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if settings.USE_CORRELATION_ID:
    from app.middlewares.correlation import CorrelationMiddleware

    app.add_middleware(CorrelationMiddleware)

if settings.DEBUG:
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next)->Response:
        logger.debug(f"{request.method}:{request.url}")
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

# Add Routers
app.include_router(api_router_v1, prefix=settings.API_V1_STR)



@app.on_event("startup")
async def on_startup():
    logger.info("Application Started")
    {%- if (cookiecutter.orm == "tortoise") or (cookiecutter.orm == "beanie") %}
    await get_db()
    {%- endif %}

    {%- if cookiecutter.orm == "mongo" %}
    await connect_to_mongo()
    {%- endif %}

    {%- if cookiecutter.enable_kafka == "True" %}
    await start_kafka(app)
    {%- endif %}

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Application Shutdown")
    {%- if cookiecutter.orm == "mongo" %}
    await close_mongo_connection()
    {%- endif %}

    {%- if cookiecutter.enable_kafka == "True" %}
    await shutdown_kafka()
    {%- endif %}

    {%- if cookiecutter.enable_redis == "True" %}
    await shutdown_redis(app)
    {%- endif %}


# Custom HTTPException handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_, exc: StarletteHTTPException) -> ORJSONResponse:
    return ORJSONResponse(
        content={
            "message": exc.detail,
        },
        status_code=exc.status_code,
        headers=exc.headers,
    )

@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(
        _,
        exc: RequestValidationError,
) -> ORJSONResponse:
    return ORJSONResponse(
        content=APIValidationError.from_pydantic(exc).dict(exclude_none=True),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )

def run_dev_server() -> None:
    """Run the uvicorn server in development environment."""
    uvicorn.run(app,
                host="127.0.0.1" if settings.DEBUG else "0.0.0.0",
                port=8000,
                reload=settings.DEBUG)

    if __name__ == "__main__":
        run_dev_server()
