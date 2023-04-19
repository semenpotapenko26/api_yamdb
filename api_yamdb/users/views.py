from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

from .models import User
from .serializers import UserSerializer, TokenSerializer, SelfCreateUserSerializer
from .utils import send_email_confirmation
from .permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для создания и получения пользователей.
    """
    http_method_names = ['get', 'patch', 'post', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=username',)


class MeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для получения и изменения своей учетки.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    @action(methods=['get', 'patch'], detail=True)
    def me(self, request):
        serializer = self.get_serializer_class()
        user = get_object_or_404(User, username=request.user.username)
        if self.request.method == 'PATCH':
            serializer = serializer(user, request.data, partial=True)
            if serializer.is_valid():
                serializer.save(role=user.role)
                return Response(
                    serializer.data, status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelfCreateUserView(generics.CreateAPIView):
    """
    Вьюкласс для самостоятельной регистрации пользователей.
    """
    queryset = User.objects.all()
    serializer_class = SelfCreateUserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, created = User.objects.get_or_create(
                **serializer.initial_data
            )
            send_email_confirmation(user)
        except IntegrityError:
            raise ValidationError()
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "email": serializer.data["email"],
                "username": serializer.data["username"],
            },
            status=status.HTTP_200_OK,
            headers=headers
        )

        # if serializer.is_valid():
        #     user = serializer.save()
        #     send_email_confirmation(user)
        #     headers = self.get_success_headers(serializer.data)
        #     return Response(
        #         {
        #             "email": serializer.data["email"],
        #             "username": serializer.data["username"],
        #         },
        #         status=status.HTTP_200_OK,
        #         headers=headers
        #     )
        # try:
        #     user, created = User.objects.get_or_create(
        #         **serializer.initial_data
        #     )
        #     if user:
        #         return Response(
        #             {
        #                 "email": user.email,
        #                 "username": user.username,
        #             },
        #             status=status.HTTP_200_OK
        #         )
        # except IntegrityError:
        #     raise ValidationError()

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes([AllowAny, ])
def get_token_view(request):
    """
    Вью-функция для получения access token.
    """
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username'],
        )
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
