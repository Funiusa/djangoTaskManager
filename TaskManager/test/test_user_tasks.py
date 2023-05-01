from http import HTTPStatus

import factory

from main.serializer import TaskSerializer
from test.base import TestViewSetBase
from test.factories import UserFactory, TaskFactory, fake


class TestUserTasksViewSet(TestViewSetBase):
    basename = "user_tasks"

    def test_list(self) -> None:
        user = UserFactory.create(role="manager")
        task1 = TaskFactory.create(assigned_by_id=user.id)
        TaskFactory.create()
        tasks = self.list(args=[user.id])
        assert tasks.status_code == HTTPStatus.OK
        serialize_task1 = TaskSerializer(task1)
        assert tasks.data == [serialize_task1.data]

    def test_retrieve_foreign_task(self) -> None:
        user = UserFactory.create()
        task = TaskFactory.create()

        response = self.request_retrieve(args=[task.id, user.id])

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_retrieve(self) -> None:
        user = UserFactory.create(role="manager")
        task = TaskFactory.create(assigned_by_id=user.id)

        retrieved_task = self.request_retrieve(args=[user.id, task.id])
        assert retrieved_task.status_code == HTTPStatus.OK
        serializer = TaskSerializer(task)
        assert serializer.data == retrieved_task.data

    def test_update(self) -> None:
        user = UserFactory.create(role="manager")
        task = TaskFactory.create(assigned_by_id=user.id, state="archived")

        update_attributes = {"state": "in_qa"}
        response = self.request_update(data=update_attributes, args=[user.id, task.id])
        assert response.status_code == HTTPStatus.OK
        assert response.data["assigned_by"] == user.username
        assert response.data["state"] == "in_qa"

    def test_delete(self) -> None:
        user = UserFactory.create(role="manager")
        task = TaskFactory.create(assigned_by_id=user.id)

        response = self.request_delete(args=[user.id, task.id])
        assert response.status_code == HTTPStatus.NO_CONTENT
