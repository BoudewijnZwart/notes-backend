from fastapi import FastAPI
import models
from database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "hello world!"}


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    return {"note-id": note_id}
