from fastapi import FastAPI

from app.api.main import api_router
from app.config import settings
from app.database import create_db_and_tables
from app.typedefs import EnvironmentType

app = FastAPI()


app.include_router(api_router)

create_db_and_tables()

if (__name__ == "__main__") and (settings.ENVIRONMENT == EnvironmentType.DEVELOPMENT):
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)  # noqa: S104
