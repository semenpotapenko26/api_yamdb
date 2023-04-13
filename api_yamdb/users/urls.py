from rest_framework import routers
from django.urls import path, include

from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path(
        'v1/users/me/',
        UserViewSet.as_view({'get': 'me', 'patch': 'me'}),
        name="user_view_set"
    ),
    path('v1/', include(router.urls)),
]
