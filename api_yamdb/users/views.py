from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для создания и получения пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(methods=['get', 'put', 'patch'], detail=True, url_path='me')
    def me(self, request, username):
        serializer = self.get_serializer_class()
        data = serializer(request.user).data
        return Response(data, status=status.HTTP_200_OK)
