import factory
from rest_framework import status
from test.base import TestViewSetBase
from test.factories import TagFactory


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)
    update_tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_list_tag(self):
        response = self.list(self.tag_attributes.get("args"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_retrieve_tag(self):
        tag = self.create(self.tag_attributes)
        tag_pk = tag.get("id")
        response = self.retrieve(tag_pk)
        self.assertEqual(response, status.HTTP_200_OK)

    def test_delete_tag(self):
        tag = self.create(self.tag_attributes)
        tag_pk = tag.get("id")
        response = self.delete(tag_pk)
        self.assertEqual(response, status.HTTP_204_NO_CONTENT)
