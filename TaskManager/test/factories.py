import factory
from faker import Faker
from main.models import Task, User, Tag, Developer
from django.contrib.auth.hashers import make_password

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    role = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in User.Roles.choices],
    )
    password = factory.LazyFunction(lambda: make_password("password"))
    date_of_birth = fake.date_of_birth().strftime("%Y-%m-%d")
    phone = fake.phone_number()[:20]


class DeveloperFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Developer

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    role = User.Roles.DEVELOPER
    is_staff = False


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    title = factory.LazyFunction(lambda: fake.word())


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = fake.sentence(nb_words=4)
    assigned_by = factory.SubFactory(UserFactory, role=User.Roles.MANAGER)
    state = Task.States.NEW
    priority = Task.Priority.LOW
    description = factory.Faker("text")
    deadline_date = fake.date_time_this_decade().strftime("%Y-%m-%dT%H:%M:%SZ")

    @factory.post_generation
    def assigned_to(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for developer in extracted:
                self.assigned_to.add(developer)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
