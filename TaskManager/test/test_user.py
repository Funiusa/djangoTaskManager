import factory
from faker import Faker
from rest_framework import status

from main.views import UserFilter
from test.base import TestViewSetBase
from test.factories import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
    updated_user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create_user(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_update_user(self):
        user = self.create(self.updated_user_attributes)
        user_pk = user.get("id")
        update_user = self.update(self.updated_user_attributes, user_pk)

        expected_response = self.expected_details(
            update_user, self.updated_user_attributes
        )
        assert update_user == expected_response

    def test_list_users(self):
        response = self.list(self.user_attributes.get("args"))
        self.assertEqual(response, status.HTTP_200_OK)

    def test_retrieve_users(self):
        user = self.create(self.user_attributes)
        user_pk = user.get("id")
        response = self.retrieve(user_pk)
        self.assertEqual(response, status.HTTP_200_OK)

    def test_delete_user(self):
        user = self.create(self.user_attributes)
        user_pk = user.get("id")
        response = self.delete(user_pk)
        self.assertEqual(response, status.HTTP_204_NO_CONTENT)


class UserFilterTestCase(TestViewSetBase):
    basename = "users"

    fake = Faker()
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
    updated_user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    def setUp(self):
        for i in range(4):
            self.user_attributes["username"] = f"john{i}"
            self.create(self.user_attributes)

    def test_filter_username(self):
        filter = UserFilter({"username": "j"})
        qs = filter.qs
        self.assertEqual(qs.count(), 4)

        filter = UserFilter({"username": "2"})
        qs = filter.qs
        self.assertEqual(qs.count(), 1)

        filter = UserFilter({"username": "xyz"})
        qs = filter.qs
        self.assertEqual(qs.count(), 0)
