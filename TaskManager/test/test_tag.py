import factory
from main.models import Tag
from test.base import TestViewSetBase
from test.factories import TagFactory


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)
    update_tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create_tag(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag == expected_response

    def test_update_tag(self):
        tag = self.create(self.update_tag_attributes)
        tag_pk = tag.get("id")
        update_tag = self.update(self.update_tag_attributes, tag_pk)

        expected_response = self.expected_details(
            update_tag, self.update_tag_attributes
        )
        assert update_tag == expected_response

    def test_list_tag(self):
        titles = ["some", "new", "tags"]
        for title in titles:
            self.tag_attributes["title"] = title
            self.create(self.tag_attributes)
        response = self.list(self.tag_attributes.get("args"))
        count = len(response.data)
        assert count == Tag.objects.count()
        response_titles = [data["title"] for data in response.data]
        assert response_titles == titles

    def test_retrieve_tag(self):
        tag = self.create(self.tag_attributes)
        tag_pk = tag.get("id")
        response = self.retrieve(tag_pk)
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert response.data == expected_response

    def test_delete_tag(self):
        tag = self.create(self.tag_attributes)
        tag_pk = tag.get("id")
        response = self.retrieve(tag_pk)
        assert response.data.get("id") == tag_pk

        response = self.delete(tag_pk)
        assert response.data is None
