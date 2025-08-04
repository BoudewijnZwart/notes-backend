import factory

from app.models.tables import Folder, Note, Tag
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
