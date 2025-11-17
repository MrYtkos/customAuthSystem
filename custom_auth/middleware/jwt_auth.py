import jwt
from django.conf import settings
from rest_framework import exceptions, authentication
from rest_framework.authentication import BaseAuthentication

from custom_auth.models import User


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        token = self.get_token_from_header(request)

        if token is None:
            token = self.get_token_from_cookie(request)

        if token is None:
            return None

        user = self.validate_token_and_get_user(token)
        return (user, None)

    def get_token_from_header(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise exceptions.AuthenticationFailed("Invalid Authorization header")

        return parts[1]

    def get_token_from_cookie(self, request):
        token = request.COOKIES.get("access_token")
        return token

    def validate_token_and_get_user(self, token):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

        user_id = payload.get("user_id")
        if not user_id:
            raise exceptions.AuthenticationFailed("Invalid payload")

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")
