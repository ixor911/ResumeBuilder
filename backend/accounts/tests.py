from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class AuthApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="alice",
            email="alice@example.com",
            password="password123",
        )

    def test_user_can_register(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "charlie",
                "email": "charlie@example.com",
                "password": "strong-password-123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["username"], "charlie")
        self.assertNotIn("first_name", response.data["user"])
        self.assertNotIn("last_name", response.data["user"])

    def test_user_can_login_and_refresh_jwt(self):
        login_response = self.client.post(
            "/api/auth/login/",
            {
                "username": "alice",
                "password": "password123",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)

        refresh_response = self.client.post(
            "/api/auth/refresh/",
            {"refresh": login_response.data["refresh"]},
            format="json",
        )

        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn("access", refresh_response.data)

    def test_authenticated_user_can_read_me(self):
        login_response = self.client.post(
            "/api/auth/login/",
            {
                "username": "alice",
                "password": "password123",
            },
            format="json",
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}"
        )
        response = self.client.get("/api/auth/me/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "alice")
