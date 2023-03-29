
import factory
from rest_framework import status

from main.models import User
from test.factories import UserFactory, TagFactory, TaskFactory
from rest_framework.test import APITestCase


class PermissionsTest(APITestCase):
    def setUp(self):
        self.admin = UserFactory(role=User.Roles.ADMIN, is_staff=True)
        self.manager = UserFactory(role=User.Roles.MANAGER, is_staff=True)
        self.developer = UserFactory(role=User.Roles.DEVELOPER, is_staff=False)
        self.tag = TagFactory()
        self.tag_data = factory.build(dict, FACTORY_CLASS=TagFactory)
        self.task_data = factory.build(
            dict,
            FACTORY_CLASS=TaskFactory,
            assigned_to=[self.developer.id],
            assigned_by=self.manager.id,
            tags=[self.tag.id],
        )

    def test_admin_can_create_tag(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post("/api/v1/tags/", self.tag_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manager_can_create_tag(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post("/api/v1/tags/", self.tag_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_developer_cannot_create_tag(self):
        self.client.force_authenticate(user=self.developer)
        response = self.client.post("/api/v1/tags/", self.tag_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_task(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post("/api/v1/tasks/", self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manager_can_create_task(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post("/api/v1/tasks/", self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_developer_cannot_create_task(self):
        self.client.force_authenticate(user=self.developer)
        response = self.client.post("/api/v1/tasks/", self.task_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
