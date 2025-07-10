from fastapi import FastAPI

from app.api.main import api_router
from app.database import create_db_and_tables

app = FastAPI()


app.include_router(api_router)

create_db_and_tables()
