from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        ]
        model = User

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Нельзя использовать имя me')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=150)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Пользователь не найден.')
        if not default_token_generator.check_token(
            user,
            data['confirmation_code'],
        ):
            raise serializers.ValidationError('Неверный код подтверждения.')
        return data
