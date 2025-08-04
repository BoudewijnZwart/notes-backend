from sqlmodel import Session, select

from app.models.tables import Tag
from tests.models.factories import NoteFactory, TagFactory


def test_note_factory(note_factory: NoteFactory, session: Session) -> None:
    del session
    note = note_factory.create()
    assert note.title is not None
    assert note.body is not None


def test_tag_factory(tag_factory: TagFactory, session: Session) -> None:
    # GIVEN a tag factory

    # WHEN a tag is created using the factory
    tag_factory.create()

    # THEN the tag should have a name
    statement = select(Tag)
    tag = session.exec(statement).first()

    assert tag.name is not None
    assert tag.id is not None


def test_tag_factory_object(tag: Tag, session: Session) -> None:
    del session
    assert tag.name is not None


def test_factory_objects_are_rolled_back(session: Session) -> None:
    """Test that objects created by factories are rolled back after the test."""
    statement = select(Tag)
    tags = session.exec(statement).all()
    assert len(tags) == 0, "Factory objects should not persist after the test"
