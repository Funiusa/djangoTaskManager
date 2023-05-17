from http import HTTPStatus

import factory
from django.core.files.uploadedfile import SimpleUploadedFile

from main.models import User
from main.views import UserFilter
from test.base import TestViewSetBase
from test.factories import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {
            **attributes,
            "id": entity["id"],
            "avatar_picture": entity["avatar_picture"],
        }

    def test_create_user(self) -> None:
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_update_user(self) -> None:
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)
        user_pk = user.get("id")
        new_user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        update_user = self.update(new_user_attributes, user_pk)
        expected_response = self.expected_details(user, new_user_attributes)
        expected_response["avatar_picture"] = update_user["avatar_picture"]
        assert update_user == expected_response

    def test_list_users(self) -> None:
        usernames = ["Ricky", "Tiki", "Tavi"]
        for username in usernames:
            user_attributes = factory.build(
                dict, FACTORY_CLASS=UserFactory, username=username
            )
            self.create(user_attributes)

        response = self.list(self.user_attributes.get("args"))
        response_usernames = [data["username"] for data in response.data]
        usernames.insert(0, self.user.username)

        assert len(response.data) == User.objects.count()
        assert response_usernames == usernames

    def test_retrieve_users(self) -> None:
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)
        user_pk = user.get("id")
        response = self.retrieve(user_pk)
        expected_response = self.expected_details(user, user_attributes)
        assert response.data == expected_response

    def test_delete_user(self) -> None:
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)
        user_pk = user.get("id")
        response = self.retrieve(user_pk)
        assert response.data.get("id") == user_pk

        response = self.delete(user_pk)
        assert response.data is None

    def test_avatar_picture(self) -> None:
        user = UserFactory.build()
        user.avatar_picture = "myavatar.png"
        user.save()
        assert user.avatar_picture is not None

    def test_large_avatar(self) -> None:
        user_attributes = factory.build(
            dict,
            FACTORY_CLASS=UserFactory,
            avatar_picture=SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024),
        )
        response = self.request_create(data=user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user_attributes["avatar_picture"].name = "bad_extension.pdf"
        response = self.request_create(data=user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }

    def get_objects_fields(self, data: dict = None, field="id") -> list:
        response = self.list(self.user_attributes.get("args"), data)
        response_obj_fields = [obj[field] for obj in response.data]
        return response_obj_fields

    def test_filter_username(self) -> None:
        names = ["john", "julia", "joh", "fiona", "donkey", "dragon"]
        for name in names:
            user_attributes = factory.build(
                dict, username=name, FACTORY_CLASS=UserFactory
            )
            self.create(user_attributes)

        qs = User.objects.all()

        for case in ["j", "d", "fiona", "shrek"]:
            params = {"username": case}
            filtered_users = UserFilter(params, queryset=qs).qs.order_by("id")
            users = [u.username for u in filtered_users]
            response = self.list(self.user_attributes.get("args"), params)
            response_users = [obj["username"] for obj in response.data]
            assert response_users == users
