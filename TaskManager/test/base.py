from http import HTTPStatus
from typing import Union, List
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from main.models import User
from faker.providers import BaseProvider


class ImageFileProvider(BaseProvider):
    def image_file(self, fmt: str = "jpeg") -> SimpleUploadedFile:
        return SimpleUploadedFile(
            self.generator.file_name(extension=fmt),
            self.generator.image(image_format=fmt),
            content_type="image/jpeg",
        )


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str
    admin: User = None

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.client = APIClient()
        cls.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="pass1234"
        )

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def authenticate_user(self, user: User) -> None:
        self.client.force_authenticate(user)

    def create(
        self, data: dict, args: List[Union[str, int]] = None, user: User = None
    ) -> dict:
        if user:
            self.authenticate_user(user)
        else:
            self.authenticate_user(self.admin)
        response = self.client.post(self.list_url(args=args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def update(
        self, data: dict, key: Union[int, str] = None, user: User = None
    ) -> dict:
        if user:
            self.authenticate_user(user)
        else:
            self.authenticate_user(self.admin)
        response = self.client.patch(
            self.detail_url(key=key), data=data, format="multipart"
        )
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def list(self, args: List[Union[str, int]] = None, user: User = None) -> dict:
        if user:
            self.authenticate_user(user)
        else:
            self.authenticate_user(self.admin)
        response = self.client.get(self.list_url(args=args))
        return response.status_code

    def retrieve(self, key: Union[int, str] = None, user: User = None) -> dict:
        if user:
            self.authenticate_user(user)
        else:
            self.authenticate_user(self.admin)
        response = self.client.get(self.detail_url(key=key))
        return response.status_code

    def delete(self, key: Union[int, str] = None, user: User = None) -> dict:
        if user:
            self.authenticate_user(user)
        else:
            self.authenticate_user(self.admin)
        response = self.client.delete(self.detail_url(key=key))
        return response.status_code
