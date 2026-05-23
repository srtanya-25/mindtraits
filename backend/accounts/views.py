"""
accounts/views.py
HTTP-only cookie JWT authentication.

Flow:
  POST /api/v1/register/   → create user
  POST /api/v1/login/      → sets access_token + refresh_token cookies
  POST /api/v1/refresh/    → reads refresh cookie, issues new access cookie
  POST /api/v1/logout/     → deletes both cookies
  GET  /api/v1/me/         → returns current user (auth required)
"""
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer


# Cookie security depends on DEBUG mode:
# - dev (DEBUG=True)   → secure=False so cookies work over http://localhost
# - prod (DEBUG=False) → secure=True (HTTPS only)
COOKIE_SECURE   = not settings.DEBUG
COOKIE_SAMESITE = "None" if not settings.DEBUG else "Lax"


def set_jwt_cookies(response, access, refresh=None):
    """Helper to set access/refresh cookies with the right flags."""
    response.set_cookie(
        key="access_token",
        value=str(access),
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        path="/",
    )
    if refresh is not None:
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            path="/",
        )
    return response


class RegisterView(generics.CreateAPIView):
    """POST /api/v1/register/ — anyone can create an account."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    """POST /api/v1/login/ — verify credentials, set HTTP-only JWT cookies."""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # authenticate() returns a User if credentials match, else None
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        # Generate refresh + access tokens from SimpleJWT
        refresh = RefreshToken.for_user(user)
        access  = refresh.access_token

        response = Response({
            "message": "Login Successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
        })
        return set_jwt_cookies(response, access, refresh)


class RefreshView(APIView):
    """POST /api/v1/refresh/ — exchange refresh cookie for a new access cookie."""
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_string = request.COOKIES.get("refresh_token")
        if not refresh_string:
            return Response({"error": "No refresh token"}, status=401)

        try:
            refresh = RefreshToken(refresh_string)
            access  = refresh.access_token

            response = Response({"message": "Token refreshed"})
            return set_jwt_cookies(response, access)
        except TokenError:
            return Response({"error": "Invalid refresh token"}, status=401)


class LogoutView(APIView):
    """POST /api/v1/logout/ — clear both cookies."""
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response({"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class MeView(APIView):
    """GET /api/v1/me/ — return the current user (used to verify auth)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })
