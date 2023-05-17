from http import HTTPStatus
from typing import Union, List, Optional
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.response import Response

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


class ActionClient:
    def __init__(self, api_client: APIClient) -> None:
        self.user: Optional[User] = None
        self.api_client = api_client

    def init_user(self):
        self.user = User.objects.create_superuser(
            username="test_admin", email="admin@example.com", password="pass1234"
        )
        self.api_client.force_authenticate(user=self.user)


class TestViewSetBase(APITestCase):
    action_client: Optional[ActionClient] = None
    api_client: APIClient = None
    basename = str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.api_client = APIClient()
        cls.action_client = ActionClient(cls.api_client)
        cls.action_client.init_user()
        cls.user = cls.action_client.user

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def detail_url_list(cls, args: List[Union[int, str]]) -> str:
        return reverse(f"{cls.basename}-detail", args=args)

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def request_create(
        self, data: dict, args: List[Union[str, int]] = None
    ) -> Response:
        url = self.list_url(args)
        return self.api_client.post(url, data=data)

    def request_update(self, data: dict, key: Union[int, str] = None) -> Response:
        url = self.detail_url(key)
        return self.api_client.patch(url, data=data)

    def request_update_list(self, data: dict, args: List[Union[int, str]]) -> Response:
        url = self.detail_url_list(args=args)
        response = self.api_client.patch(url, data=data)
        return response

    def request_delete_list(self, args: List[Union[int, str]]) -> Response:
        url = self.detail_url_list(args=args)
        response = self.api_client.delete(url)
        return response

    def request_retrieve_list(self, args: List[Union[int, str]]) -> Response:
        url = self.detail_url_list(args=args)
        response = self.api_client.get(url)
        return response

    def request_list(
        self, args: List[Union[str, int]] = None, data: dict = None
    ) -> Response:
        url = self.list_url(args)
        return self.api_client.get(url, data)

    def request_retrieve(self, key: Union[int, str] = None) -> Response:
        url = self.detail_url(key)
        return self.api_client.get(url)

    def request_delete(self, key: Union[int, str] = None) -> Response:
        url = self.detail_url(key)
        return self.api_client.delete(url)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.request_create(data, args)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def update(self, data: dict, key: Union[int, str] = None) -> dict:
        response = self.request_update(data, key)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def list(self, args: List[Union[str, int]] = None, data: dict = None) -> Response:
        response = self.request_list(args, data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response

    def retrieve(self, key: Union[int, str] = None) -> Response:
        response = self.request_retrieve(key)
        assert response.status_code == HTTPStatus.OK, response.content
        return response

    def delete(self, key: Union[int, str] = None) -> Response:
        response = self.request_delete(key)
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        return response

    def request_single_resource(self, data: dict = None) -> Response:
        return self.api_client.get(self.list_url(), data=data)

    def single_resource(self, data: dict = None) -> dict:
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def request_patch_single_resource(self, attributes: dict) -> Response:
        return self.api_client.patch(self.list_url(), data=attributes)

    def patch_single_resource(self, attributes: dict) -> dict:
        response = self.request_patch_single_resource(attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data
