from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import User
from .serializers import UserSerializer, TokenSerializer
from .utils import send_email_confirmation


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для создания и получения пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=True)
    def me(self, request):
        serializer = self.get_serializer_class()
        user = get_object_or_404(User, username=request.user.username)
        if self.request.method == 'PATCH':
            serializer = serializer(user, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelfCreateUser(generics.CreateAPIView):
    """
    Вьюкласс для самостоятельной регистрации пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        send_email_confirmation(user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "Message": "Мы отправили на указанный вами "
                "адрес код для получения токена."
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


@api_view(['POST',])
def get_token(request):
    """
    Вью-функция для получения access token.
    """
    # нужно проверить токен и username
    # выдать токен
    if request.method == 'POST':
        # Создаём объект сериализатора 
        # и передаём в него данные из POST-запроса
        serializer = CatSerializer(data=request.data)
        if serializer.is_valid():
            # Если полученные данные валидны —
            # сохраняем данные в базу через save().
            serializer.save()
            # Возвращаем JSON со всеми данными нового объекта
            # и статус-код 201
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Если данные не прошли валидацию — 
        # возвращаем информацию об ошибках и соответствующий статус-код:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)