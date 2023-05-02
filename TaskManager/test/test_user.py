from http import HTTPStatus

import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse

from main.views import UserFilter
from test.base import TestViewSetBase
from test.factories import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"

    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
    updated_user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {
            **attributes,
            "id": entity["id"],
            "avatar_picture": entity["avatar_picture"],
        }

    def test_create_user(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_update_user(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)
        user_pk = user.get("id")
        new_user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        update_user = self.update(new_user_attributes, user_pk)
        expected_response = self.expected_details(user, new_user_attributes)
        expected_response["avatar_picture"] = update_user["avatar_picture"]
        assert update_user == expected_response

    def test_list_users(self):
        response = self.list(self.user_attributes.get("args"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_users(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)
        user_pk = user.get("id")
        response = self.retrieve(user_pk)
        self.assertEqual(response, status.HTTP_200_OK)

    def test_delete_user(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)
        user_pk = user.get("id")
        response = self.delete(user_pk)
        self.assertEqual(response, status.HTTP_204_NO_CONTENT)

    def test_avatar_picture(self):
        user = UserFactory.build()
        user.avatar_picture = "myavatar.png"
        user.save()
        self.assertIsNotNone(user.avatar_picture)

    def test_large_avatar(self) -> None:
        user_attributes = factory.build(
            dict,
            FACTORY_CLASS=UserFactory,
            avatar_picture=SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024),
        )
        self.client.force_authenticate(self.admin)
        response = self.client.post(reverse("users-list"), data=user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user_attributes["avatar_picture"].name = "bad_extension.pdf"
        self.client.force_authenticate(self.admin)
        response = self.client.post(reverse("users-list"), data=user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }


class UserFilterTestCase(TestViewSetBase):
    basename = "users"

    def setUp(self):
        for i in range(4):
            user_attributes = factory.build(
                dict, username=f"john{i}", FACTORY_CLASS=UserFactory
            )
            self.create(user_attributes)

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
