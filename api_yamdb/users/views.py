from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import TokenSerializer, UserSerializer
from .utils import send_email_confirmation


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для создания и получения пользователей.
    """
    http_method_names = ['get', 'patch', 'post', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('=username',)


class MeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для получения и изменения своей учетки.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['patch'])
    def me(self, request):
        """Change user info partial."""
        serializer = self.get_serializer_class()
        user = get_object_or_404(User, username=request.user.username)
        serializer = serializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @me.mapping.get
    def get_me(self, request):
        """Get user info."""
        serializer = self.get_serializer_class()
        user = get_object_or_404(User, username=request.user.username)
        serializer = serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SelfCreateUserView(generics.CreateAPIView):
    """
    Вьюкласс для самостоятельной регистрации пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        COUNT_UNIQUE_ERROR = 2

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            if (
                len(exc.detail) == COUNT_UNIQUE_ERROR
                and exc.detail['username'][0].code == 'unique'
                and exc.detail['email'][0].code == 'unique'
            ):
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        user = serializer.save()
        send_email_confirmation(user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


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
