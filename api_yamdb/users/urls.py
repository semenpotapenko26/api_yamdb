from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserViewSet, SelfCreateUser, GetToken

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path(
        'v1/users/me/',
        UserViewSet.as_view({'get': 'me', 'patch': 'me'}),
        name="user_view_set"
    ),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SelfCreateUser.as_view()),
    path('v1/auth/token/', GetToken.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
