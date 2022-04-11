from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class AuthAppSetUpTestCase(APITestCase):

    def setUp(self):
        self.user_data = {
            "email": "some@gmail.com",
            "username": "some_username",
            "password": "fortest2020",
            "password2": "fortest2020"
        }

        self.user = User.objects.create(
            username=self.user_data['username'],
            email=self.user_data['email'],
        )
        self.user.set_password(self.user_data["password"])
        self.user.save()


class BearerTokenTestCaseBase(AuthAppSetUpTestCase):
    @property
    def bearer_token(self):
        user = User.objects.get(id=self.user.id)
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}


class TestAuthView(AuthAppSetUpTestCase):

    def test_user_can_sign_up(self):
        sign_up_url = reverse("auth_sign_up")

        self.user_data["email"] = "some2@gmail.com"
        self.user_data["username"] = "some_username_2"

        res = self.client.post(sign_up_url, self.user_data)
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_sign_up(self):
        sign_up_url = reverse("auth_sign_up")
        res = self.client.post(sign_up_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_login(self):
        login_url = reverse("token_obtain_pair")
        user_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }

        res = self.client.post(login_url, user_data)
        self.assertEqual(res.status_code, 200)

    def test_user_cannot_login_incorrect_creds(self):
        login_url = reverse("token_obtain_pair")
        user_data = {
            "email": "unexisting@gmail.com",
            "password": "fortest2020",
        }

        res = self.client.post(login_url, user_data)
        self.assertEqual(res.status_code, 403)


class TestUserView(BearerTokenTestCaseBase):

    def test_user_data_api(self):
        user_data_url = reverse("user_data", args=[self.user.id])
        res = self.client.get(
            user_data_url, **self.bearer_token
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.user.email, res.data["email"])
        self.assertEqual(self.user.username, res.data["username"])
