from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

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


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username',]
        model = User
        # read_only = ['username',]

    def validate(self, value):
        pass
