import bcrypt
from rest_framework import serializers
from custom_auth.models import User, Role


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'role',
            'is_active'
        ]

        read_only_fields = ['role', 'is_active']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
                'first_name', 'last_name', 'middle_name',
                'email', 'password', 'password_repeat'
            ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_repeat')

        raw_password = validated_data.pop('password')
        hashed = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()
        validated_data['password'] = hashed

        validated_data.pop('role', None)

        user_role, _ = Role.objects.get_or_create(role_name='user')
        validated_data['role'] = user_role

        return User.objects.create(**validated_data)


class UserSoftDeleteSerializer(serializers.Serializer):
    confirm = serializers.BooleanField()

    def validate_confirm(self, value):
        if value is not True:
            raise serializers.ValidationError("Подтвердите удаление")
        return value


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'middle_name'
        ]
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'middle_name': {'required': False},
        }


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password_repeat = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user

        if not bcrypt.checkpw(
            attrs['current_password'].encode(),
            user.password.encode()
        ):
            raise serializers.ValidationError("Текущий пароль неверный")

        if attrs['new_password'] != attrs['new_password_repeat']:
            raise serializers.ValidationError("Пароли не совпадают")

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user

        raw = self.validated_data['new_password']
        hashed = bcrypt.hashpw(raw.encode(), bcrypt.gensalt()).decode()

        user.password = hashed
        user.save()

        return user
