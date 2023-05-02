from test.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "current_user"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def test_retrieve(self):
        user = self.single_resource()

        assert user == {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "role": self.user.role,
            "username": self.user.username,
            "password": self.user.password,
            "avatar_picture": self.user.avatar_picture,
            "date_of_birth": self.user.date_of_birth,
            "phone": self.user.phone,
        }

    def test_patch(self):
        self.patch_single_resource({"first_name": "TestName"})

        user = self.single_resource()
        assert user["first_name"] == "TestName"
