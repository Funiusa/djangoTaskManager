import factory
from rest_framework import status
from main.models import Task, Tag
from main.serializer import TagSerializer
from test.base import TestViewSetBase
from test.factories import TaskFactory, TagFactory


class TestTaskTagsViewSet(TestViewSetBase):
    basename = "task_tags"
    tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

    def setUp(self):
        self.task = TaskFactory.create()
        self.tag1 = TagFactory.create()
        self.tag2 = TagFactory.create()

    def test_create(self) -> None:
        tag = self.create(data=self.tag_attributes, args=[self.task.id])
        tag_id = tag.get("id")
        tag = Tag.objects.get(pk=tag_id)
        assert tag.title == self.tag_attributes.get("title")

    def test_update(self) -> None:
        self.add_tags(self.task, [self.tag1])
        tag_id = self.tag1.id
        new_title = "New Tag Title"
        updated_data = {"title": new_title}
        response = self.request_update_list(
            data=updated_data, args=[self.task.id, tag_id]
        )
        updated_tag = self.task.tags.filter(pk=tag_id).first()
        assert response.status_code == status.HTTP_200_OK
        serializer_tag = TagSerializer(updated_tag)
        assert response.data == serializer_tag.data

    def test_delete(self) -> None:
        self.add_tags(self.task, [self.tag1, self.tag2])
        response = self.request_delete_list(args=[self.task.id, self.tag1.id])
        assert response.status_code == status.HTTP_204_NO_CONTENT

        self.task.refresh_from_db()
        assert self.tag1 not in self.task.tags.all()

    def test_list(self) -> None:
        self.add_tags(self.task, [self.tag1, self.tag2])

        tags = self.list(args=[self.task.id])
        assert tags.status_code == status.HTTP_200_OK
        serializers = [TagSerializer(self.tag1).data, TagSerializer(self.tag2).data]
        assert tags.data == serializers

    def test_retrieve(self) -> None:
        self.add_tags(self.task, [self.tag1, self.tag2])
        retrieved_tag = self.request_retrieve_list(args=[self.task.id, self.tag2.id])
        assert retrieved_tag.status_code == status.HTTP_200_OK

    @staticmethod
    def add_tags(task: dict, tags: list) -> None:
        ids = [tag.id for tag in tags]
        task_instance = Task.objects.get(pk=task.id)
        task_instance.tags.add(*ids)
        task_instance.save()
