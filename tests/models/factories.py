from typing import Any

import factory

from app.models.tables import Folder, Note, Tag, User
from app.security import get_password_hash
from tests.factories import ModelFactory


class NoteFactory(ModelFactory):
    class Meta:
        model = Note

    title = factory.Faker("sentence", nb_words=4)
    body = factory.Faker("text", max_nb_chars=200)


class TagFactory(ModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker("word")


class FolderFactory(ModelFactory):
    class Meta:
        model = Folder

    name = factory.Faker("word")


class UserFactory(ModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    hashed_password = factory.LazyFunction(lambda: get_password_hash("Password123!"))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_superuser = False

    @classmethod
    def create(cls, **kwargs: Any) -> User:
        """Override create to accept plain 'password' and hash it."""
        password = kwargs.pop("password", None)
        if password:
            kwargs["hashed_password"] = get_password_hash(password)
        return super().create(**kwargs)
