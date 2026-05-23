from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Reads JWT access token from HTTP-only cookie instead of Authorization header.
        Returns None silently if no token found (sets request.user to AnonymousUser).
        """
        token = request.COOKIES.get("access_token")
        if not token:
            return None

        validated_token = self.get_validated_token(token)
        user = self.get_user(validated_token)
        return user, validated_token
