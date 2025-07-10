from fastapi import FastAPI

from app.database import create_db_and_tables
from app.api.main import api_router

app = FastAPI()


app.include_router(api_router)

create_db_and_tables()
