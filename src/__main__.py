import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from uvicorn import run

from src.config import get_settings, Settings
from src.routers import list_of_routes
from src.utils.exceptions import BaseAPIException
from src.utils.healthcheck import Healthcheck

settings: Settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Healthcheck.check_dependencies()
    yield


def bind_routes(application: FastAPI, settings: Settings) -> None:
    for route in list_of_routes:
        application.include_router(route, prefix=settings.PATH_PREFIX)


def get_app() -> FastAPI:
    title = 'Incident Service'
    description = 'API service for incident management'
    version = '0.1.0'
    docs_url = '/docs'
    redoc_url = '/redoc'
    log_config = settings.logging_config
    logging.config.dictConfig(log_config)

    application: FastAPI = FastAPI(
        title=title,
        description=description,
        version=version,
        default_response_class=ORJSONResponse,
        docs_url=docs_url,
        redoc_url=redoc_url,
        lifespan=lifespan,
        log_config=log_config,
    )

    origins = ['*']
    methods = ['*']
    headers = ['*']
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=methods,
        allow_headers=headers,
    )
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app: FastAPI = get_app()


@app.exception_handler(BaseAPIException)
async def exception_handler(
    request: Request,
    exc: BaseAPIException
) -> ORJSONResponse:
    logging.error(
        f'API Exception: {exc.__class__.__name__}',
        extra={
            'message': exc.message,
            'status_code': exc.status_code,
            'detail': exc.detail,
            'path': request.url.path,
        }
    )
    return ORJSONResponse(
        status_code=exc.status_code,
        content=exc.to_response().model_dump(),
    )


if __name__ == "__main__":
    settings_for_application: Settings = get_settings()   
    run(
        "src.__main__:app",
        host="127.0.0.1",
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=["src", "tests"],
        log_level="debug",
        workers=1,
    )
