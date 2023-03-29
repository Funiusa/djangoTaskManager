import factory
from faker import Faker
from main.models import Task, User, Tag
from django.contrib.auth import get_user_model

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "test1234")
    role = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in User.Roles.choices],
    )


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    title = factory.LazyFunction(lambda: fake.word())


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = "new"
    assigned_by = factory.SubFactory(
        UserFactory, role=User.Roles.MANAGER, is_staff=True
    )
    assigned_to = factory.SubFactory(
        UserFactory, role=User.Roles.DEVELOPER, is_staff=False
    )
    tags = factory.SubFactory(TagFactory)
    description = "Some description"
    deadline_date = "2023-04-01T00:00:00Z"
    state = Task.States.NEW
    priority = Task.Priority.LOW
