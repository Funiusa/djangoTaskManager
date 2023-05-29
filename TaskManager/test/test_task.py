import factory
from main.models import User, Task, Tag
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

    def create_objects_list(self, attributes: list, user: User = None) -> None:
        if user:
            self.api_client.force_authenticate(user)
        for attr in attributes:
            self.task_attributes.update(attr)
            self.create(self.task_attributes)

    def get_objects_fields(self, data: dict = None, field="id") -> list:
        response = self.list(self.task_attributes.get("args"), data)
        response_obj_fields = [obj[field] for obj in response.data]
        return response_obj_fields

    def test_list_task(self):
        attributes = [{"title": fake.sentence(nb_words=num)} for num in range(1, 5)]
        self.create_objects_list(attributes)
        titles = list(Task.objects.all().values_list("title", flat=True))
        response_tasks_titles = self.get_objects_fields(field="title")
        assert response_tasks_titles == titles

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
        attributes = [{"state": attr} for attr in state_list]
        self.create_objects_list(attributes)

        qs = Task.objects.all()
        for state in ["rel", "new", "in"]:
            filter_options = {"state": state}
            filtered_qs = TaskFilter(filter_options, queryset=qs).qs
            filtered_task_ids = list(filtered_qs.values_list("id", flat=True))
            response_ids = self.get_objects_fields(filter_options)
            assert filtered_task_ids == response_ids

    def test_task_filter_assigned_by(self):
        for num in range(1, 5):
            attributes = [{"title": fake.sentence(nb_words=num)}]
            manager = UserFactory(role=User.Roles.MANAGER, is_staff=True)
            self.create_objects_list(attributes, manager)

        qs = Task.objects.all()
        managers = User.objects.filter(is_staff=True).values_list("username", flat=True)

        for manager in managers:
            filter_options = {"assigned_by": manager}
            filtered_qs = TaskFilter(filter_options, queryset=qs).qs
            filtered_task_ids = list(filtered_qs.values_list("id", flat=True))
            response_ids = self.get_objects_fields(filter_options)
            assert filtered_task_ids == response_ids

    def test_task_filter_assigned_to(self):
        for num in range(1, 5):
            dev = UserFactory(role=User.Roles.DEVELOPER, is_staff=False)
            attributes = [{"title": fake.sentence(nb_words=num), "assigned_to": dev}]
            self.create_objects_list(attributes)

        qs = Task.objects.all()
        devs = User.objects.filter(is_staff=False).values_list("username", flat=True)
        for dev in devs:
            filter_options = {"assigned_to": dev}
            filtered_qs = TaskFilter(filter_options, queryset=qs).qs
            filtered_task_ids = list(filtered_qs.values_list("id", flat=True))
            response_ids = self.get_objects_fields(filter_options)
            assert filtered_task_ids == response_ids

    def test_task_filter_tag(self):
        for num in range(1, 5):
            tag = TagFactory(title=fake.word())
            attributes = [{"title": fake.sentence(nb_words=num), "tag": tag}]
            self.create_objects_list(attributes)

        tags = Tag.objects.all()
        qs = Task.objects.all()
        for tag in tags:
            filter_options = {"tags": tag}
            filtered_qs = TaskFilter(filter_options, queryset=qs).qs
            filtered_task_ids = list(filtered_qs.values_list("id", flat=True))
            response_ids = self.get_objects_fields(filter_options)
            assert filtered_task_ids == response_ids
