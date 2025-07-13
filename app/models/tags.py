from typing import Optional, Self

from sqlmodel import Field, Relationship, SQLModel

from app.shared.constants import MAX_NAME_LEN, MIN_NAME_LEN


class TagBase(SQLModel):
    """Base model for a tag."""


class Tag(TagBase, table=True):
    """Represents a tag used to group notes."""

    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(min_length=MIN_NAME_LEN, max_length=MAX_NAME_LEN)
    parent_id: int | None = Field(foreign_key="tag.id", default=None)
    parent_tag: Optional["Tag"] = Relationship(
        back_populates="child_tags",
        sa_relationship_kwargs={"remote_side": "Tag.id"},
    )
    child_tags: list["Tag"] = Relationship(back_populates="parent_tag")

    def get_full_name(self) -> str:
        """Get the full name of a tag."""
        full_name = self.name
        if self.parent_tag is not None:
            full_name = self.parent_tag.get_full_name() + "/" + full_name
        return full_name

    @staticmethod
    def full_name_to_tag_names(full_name: str) -> list[str]:
        """Split a given full tag name into separate tag names."""
        return [part for part in full_name.strip().split("/") if part]


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
        )
