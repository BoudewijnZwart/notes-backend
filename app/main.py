from fastapi import FastAPI

import app.database as database
from app.api.main import api_router

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

app.include_router(api_router)
