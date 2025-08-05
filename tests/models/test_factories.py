from sqlmodel import Session, select

from app.models.tables import Tag, User
from tests.models.factories import NoteFactory, TagFactory, FolderFactory, UserFactory


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


def test_folder_factory(folder_factory: FolderFactory, session: Session) -> None:
    # GIVEN a folder factory

    # WHEN a folder is created using the factory
    folder = folder_factory.create()

    # THEN the folder should have a name
    assert folder.name is not None
    assert folder.id is not None


def test_factory_objects_are_rolled_back(session: Session) -> None:
    """Test that objects created by factories are rolled back after the test."""
    statement = select(Tag)
    tags = session.exec(statement).all()
    assert len(tags) == 0, "Factory objects should not persist after the test"


def test_user_factory(user_factory: UserFactory, session: Session) -> None:
    """Test that the user factory creates a user with a hashed password."""
    # GIVEN a user factory

    # WHEN a user is created using the factory
    user = user_factory.create()

    # THEN the user should be in the database
    user_from_db = session.get(User, user.id)
    assert user_from_db is not None

    # AND the user should have the expected attributes
    assert user_from_db.email == user.email
    assert user_from_db.hashed_password is not None
    assert user_from_db.first_name == user.first_name
    assert user_from_db.last_name == user.last_name
