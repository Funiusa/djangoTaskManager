import factory
from rest_framework import status
from main.models import User
from main.views import TaskFilter
from test.base import TestViewSetBase
from test.factories import TaskFactory, UserFactory, TagFactory, fake


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"

    def setUp(self):
        self.manager = UserFactory(role=User.Roles.MANAGER, is_staff=True)
        self.developer = UserFactory(role=User.Roles.DEVELOPER, is_staff=False)
        self.tag = TagFactory()
        self.tags = [factory.build(dict, FACTORY_CLASS=TagFactory) for _ in range(3)]
        self.task_attributes = factory.build(
            dict,
            FACTORY_CLASS=TaskFactory,
            assigned_to=[self.developer.username],
            assigned_by=self.user.username,
            state="new_task",
            priority="low",
            tags=[self.tag.title],
        )
        self.update_task_attributes = factory.build(
            dict,
            FACTORY_CLASS=TaskFactory,
            assigned_to=[self.developer.username],
            assigned_by=self.user.username,
            state="in_qa",
            priority="high",
            tags=[self.tag.title],
        )

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_list_task(self):
        response = self.list(self.task_attributes.get("args"))
        assert response.status_code == status.HTTP_200_OK

    def test_create_task(self):
        task = self.create(self.task_attributes)
        expected_response = self.expected_details(task, self.task_attributes)
        assert task == expected_response

    def test_update_task(self):
        task = self.create(self.update_task_attributes)
        task_pk = task.get("id")
        update_task = self.update(self.update_task_attributes, task_pk)

        expected_response = self.expected_details(
            update_task, self.update_task_attributes
        )
        assert update_task == expected_response

    def test_retrieve_task(self):
        task = self.create(self.task_attributes)
        task_pk = task.get("id")
        response = self.retrieve(task_pk)
        expected_response = self.expected_details(task, self.task_attributes)
        assert expected_response == response.data

    def test_delete_task(self):
        task = self.create(self.task_attributes)
        task_pk = task.get("id")
        response = self.retrieve(task_pk)
        assert response.data.get("id") == task_pk

        response = self.delete(task_pk)
        assert response.data is None

    def test_task_filter_state(self):
        state_list = [
            "new_task",
            "in_development",
            "in_qa",
            "new_task",
            "released",
            "released",
            "released",
        ]
        for state in state_list:
            self.task_attributes["state"] = state
            self.create(self.task_attributes)

        filter = TaskFilter({"state": "new_task"})
        qs = filter.qs
        assert qs.count() == 2

        filter = TaskFilter({"state": "released"})
        qs = filter.qs
        assert qs.count() == 3

        filter = TaskFilter({"state": "in_qa"})
        qs = filter.qs
        assert qs.count() == 1

    def test_task_filter_assigned_by(self):
        manager1 = UserFactory(
            username="manager1", role=User.Roles.MANAGER, is_staff=True
        )
        manager3 = UserFactory(
            username="manager3", role=User.Roles.MANAGER, is_staff=True
        )
        managers = [manager1, manager1, manager3]
        for i in range(3):
            self.task_attributes["title"] = fake.sentence(nb_words=2)
            self.api_client.force_authenticate(managers[i])
            self.create(self.task_attributes)

        filter = TaskFilter({"assigned_by": "manager1"})
        qs = filter.qs
        assert qs.count() == 2

        filter = TaskFilter({"assigned_by": "manager3"})
        qs = filter.qs
        assert qs.count() == 1

        filter = TaskFilter({"assigned_by": "manager2"})
        qs = filter.qs
        assert qs.count() == 0

    def test_task_filter_assigned_to(self):
        developer1 = UserFactory(
            username="dev1", role=User.Roles.DEVELOPER, is_staff=False
        )
        developer2 = UserFactory(
            username="dev2", role=User.Roles.DEVELOPER, is_staff=False
        )
        executors = [developer1, developer2, developer1]

        for i in range(3):
            self.task_attributes["title"] = fake.sentence(nb_words=2)
            self.task_attributes["assigned_to"] = executors[i]
            self.create(self.task_attributes)

        filter = TaskFilter({"assigned_to": "dev1"})
        qs = filter.qs
        assert qs.count() == 2

        filter = TaskFilter({"assigned_to": "dev2"})
        qs = filter.qs
        assert qs.count() == 1

    def test_task_filter_tag(self):
        tag1 = TagFactory(title="fix")
        tag2 = TagFactory(title="create")
        tags = [tag1, tag2, tag1]
        for i in range(3):
            self.task_attributes["title"] = fake.sentence(nb_words=2)
            self.task_attributes["tags"] = tags[i]
            self.create(self.task_attributes)

        filter = TaskFilter({"tags": "fix"})
        qs = filter.qs
        assert qs.count() == 2

        filter = TaskFilter({"tags": "create"})
        qs = filter.qs
        assert qs.count() == 1

        filter = TaskFilter({"tags": "update"})
        qs = filter.qs
        assert qs.count() == 0
