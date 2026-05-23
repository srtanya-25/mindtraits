from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Reads JWT access token from HTTP-only cookie instead of Authorization header.
        Returns None (anonymous) if the cookie is missing, expired, or invalid -
        so a stale cookie never breaks public endpoints like login.
        """
        token = request.COOKIES.get("access_token")
        if not token:
            return None

        try:
            validated_token = self.get_validated_token(token)
        except (InvalidToken, TokenError):
            return None

        user = self.get_user(validated_token)
        return user, validated_token
