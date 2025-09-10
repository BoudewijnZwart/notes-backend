from typing import Self

from sqlmodel import Field

from app.models.basemodels import TagBase
from app.models.tables import Tag
from app.shared.constants import MAX_NAME_LEN, MIN_NAME_LEN


class TagNew(TagBase):
    """Schema for a new tag."""

    full_name: str = Field(min_length=MIN_NAME_LEN, max_length=MAX_NAME_LEN)


class TagPublic(TagBase):
    """Schema for a tag returned to the user."""

    id: int
    name: str
    full_name: str
    parent_id: int | None
    child_ids: list[int]

    @classmethod
    def from_tag(cls, tag: Tag) -> Self:
        """Create a TagPublic from a Tag."""
        if Tag.id is None:
            msg = "Missing primary key."
            raise ValueError(msg)

        return cls(
            id=tag.id,
            name=tag.name,
            full_name=tag.get_full_name(),
            parent_id=tag.parent_id,
            child_ids=[child.id for child in tag.child_tags],
            owner_id=tag.owner_id,
        )
