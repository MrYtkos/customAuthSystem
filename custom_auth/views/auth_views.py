import jwt
import datetime
from django.conf import settings
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_auth.models import User, Session
from custom_auth.serializers import (
    UserProfileSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
    UserRegistrationSerializer,
    UserSoftDeleteSerializer, ChangePasswordSerializer
)


def create_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=3),
        'iat': datetime.datetime.now(datetime.UTC)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({"error": "Неверные учетные данные"}, status=status.HTTP_400_BAD_REQUEST)

        token = create_jwt(user.user_id)

        Session.objects.create(
            user_id=user.user_id,
            token=token,
            expires_at=timezone.now() + datetime.timedelta(hours=3)
        )

        response = Response({"message": "Login successfully"}, status=200)
        response.set_cookie(
            key='access_token',
            value=token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        return response


class LogoutView(APIView):
    def post(self, request):
        token = request.COOKIES.get('access_token')

        if token:
            Session.objects.filter(token=token).delete()

        response = Response({"message": "Logout successfully"}, status=200)
        response.delete_cookie('access_token')
        return response


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Пароль обновлён успешно"}, status=200)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()

        # Если используем cookie для токена — удаляем его
        response = Response({"message": "Пользователь удалён"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        return response

