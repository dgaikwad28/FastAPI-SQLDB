from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.configs.session import engine
from app.configs.settings import SETTINGS
from app.exception_handlers import InvalidData, handler_uncaught_exception, incorrect_configuration, invalid_data
from app.logging import logging_config
from app.models.db_models import Base
from app.routers.router import users_api_router


def get_logger():
    config = logging_config()
    if config:
        dictConfig(config)


def init_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)

    # setup logging
    get_logger()

    _app = FastAPI(debug=SETTINGS.debug)
    # exceptions
    _app.add_exception_handler(InvalidData, invalid_data)
    _app.add_exception_handler(RequestValidationError, incorrect_configuration)
    _app.add_exception_handler(Exception, handler_uncaught_exception)

    # middlewares
    _app.add_middleware(SessionMiddleware, https_only=SETTINGS.https_only, secret_key=SETTINGS.secret_key,
                        same_site="strict")
    _app.add_middleware(TrustedHostMiddleware, allowed_hosts=SETTINGS.allowed_hosts)

    # routers
    _app.include_router(users_api_router)

    return _app


app = init_app()
