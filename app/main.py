from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.main import api_router
from app.config import settings
from app.startup import startup
from app.typedefs import EnvironmentType


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001, ANN201
    """Lifespan context manager for FastAPI app."""
    # Startup code
    startup()

    yield
    # Shutdown code (if any) can be added here


app = FastAPI(lifespan=lifespan)


app.include_router(api_router)


# use uvicorn to run the app in development
if (__name__ == "__main__") and (settings.ENVIRONMENT == EnvironmentType.DEVELOPMENT):
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)  # noqa: S104
