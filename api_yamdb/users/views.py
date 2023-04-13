from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSerializer


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
