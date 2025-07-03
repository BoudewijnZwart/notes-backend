from pydantic import BaseModel
from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    private = Column(Boolean, default=False)
