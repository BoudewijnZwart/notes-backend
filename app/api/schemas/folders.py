from sqlmodel import Field

from app.models.basemodels import FolderBase


class FolderNew(FolderBase):
    """Schema for a new folder."""

    parent_id: int | None = Field(default=None)


class FolderPublic(FolderBase):
    """Schema for a folder returned to the public."""

    id: int
    parent_id: int | None
