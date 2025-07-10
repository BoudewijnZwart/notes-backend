from sqlmodel import Field, SQLModel


class NoteBase(SQLModel):
    title: str = Field()
    body: str = Field()
    folder: int | None = Field(
        foreign_key="folder.id", default=None, ondelete="CASCADE"
    )


class Note(NoteBase, table=True):
    id: int | None = Field(primary_key=True, default=None)


class NotePublic(NoteBase):
    id: int


class NoteNew(NoteBase):
    pass


class NoteUpdate(NoteBase):
    title: str | None = None
    body: str | None = None
    folder: str | None = None
