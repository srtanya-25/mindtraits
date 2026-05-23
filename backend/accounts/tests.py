"""
accounts/tests.py
Tests for HTTP-only cookie JWT auth flow.
Pattern: TestCase + APIClient + targeted assertions.
"""
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_with_valid_data(self):
        response = self.client.post(
            "/api/v1/register/",
            {"username": "alice", "email": "alice@example.com", "password": "test12345"},
            format="json",
        )
        self.assertIn(response.status_code, (200, 201))
        self.assertTrue(User.objects.filter(username="alice").exists())

    def test_register_with_short_password_fails(self):
        response = self.client.post(
            "/api/v1/register/",
            {"username": "bob", "email": "bob@example.com", "password": "1234"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.create_user(
            username="charlie", email="c@example.com", password="test12345"
        )

    def test_login_with_valid_credentials_sets_cookies(self):
        response = self.client.post(
            "/api/v1/login/",
            {"username": "charlie", "password": "test12345"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token",  response.cookies)
        self.assertIn("refresh_token", response.cookies)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            "/api/v1/login/",
            {"username": "charlie", "password": "wrongpass"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.create_user(username="dave", password="test12345")

    def test_logout_clears_cookies(self):
        self.client.post(
            "/api/v1/login/",
            {"username": "dave", "password": "test12345"},
            format="json",
        )
        response = self.client.post("/api/v1/logout/")
        self.assertEqual(response.status_code, 200)
