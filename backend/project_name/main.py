import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pytz import timezone

from project_name.configs import PROJECT_NAME_CAPS_HOST
from project_name.configs import PROJECT_NAME_CAPS_PORT
from project_name.modules.auth.api import router as auth_router
from project_name.modules.email.api import router as email_router
from project_name.modules.user.api import router as user_router
from project_name.utils.logging import setup_logger

logger = setup_logger()


def get_application() -> FastAPI:
    application = FastAPI(root_path="/api", redirect_slashes=True)
    scheduler = BackgroundScheduler()

    # API Routes
    application.include_router(auth_router)
    application.include_router(user_router)
    application.include_router(email_router)

    # Middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
        logger.exception(f"{request}: {exc_str}")
        return JSONResponse(
            status_code=422,
            content={"message": exc_str, "data": None},
        )

    @application.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
        logger.exception(f"{request}: {exc_str}")
        return JSONResponse(
            status_code=400,
            content={"message": exc_str, "data": None},
        )

    return application


app = get_application()

if __name__ == "__main__":
    logger.info(
        f"Starting project_name on http://{PROJECT_NAME_CAPS_HOST}:{str(PROJECT_NAME_CAPS_PORT)}/"
    )
    uvicorn.run(app, host=PROJECT_NAME_CAPS_HOST, port=PROJECT_NAME_CAPS_PORT)
