from http import HTTPStatus
from typing import Type, Container
from django.db import models
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from main.models import User, Task, Tag
import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Sequence(lambda n: 'Task %d' % n)
    description = 'Some description'
    assigned_by = factory.SubFactory(UserFactory)
    deadline_date = factory.Faker('future_date')
    state = 'new_task'
    priority = factory.Faker('random_int', min=1, max=5)

    @factory.post_generation
    def assigned_to(self, create, extracted, **kwargs):
        if create:
            return
        if extracted:
            for user in extracted:
                self.assigned_to.add(user)
        else:
            self.assigned_to.add(UserFactory)


class TestAdmin(APITestCase):
    client: APIClient
    admin: User

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.admin = User.objects.create_superuser(
            "test@test.ru", email=None, password=None,
        )
        cls.client = APIClient()
        cls.client.force_login(cls.admin)

    @classmethod
    def assert_forms(
            cls, model: Type[models.Model], key: int, check_actions: Container = ()
    ) -> None:
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        actions = {"changelist": [], "add": [], "change": (key,)}
        if check_actions:
            actions = {key: val for key, val in actions.items() if key in check_actions}

        for action, args in actions.items():
            url = reverse(f"admin:{app_label}_{model_name}_{action}", args=args)
            response = cls.client.get(url)
            assert response.status_code == HTTPStatus.OK, response.content

    def test_user(self) -> None:
        self.assert_forms(User, self.admin.id)

    def test_tag(self) -> None:
        tag = Tag.objects.create()
        self.assert_forms(Tag, tag.id)

    def test_task(self) -> None:
        task = Task.objects.create()
        self.assert_forms(Task, task.id)

