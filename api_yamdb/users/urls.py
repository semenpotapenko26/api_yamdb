from django.urls import include, path
from rest_framework import routers

from .views import MeViewSet, SelfCreateUserView, UserViewSet, get_token_view

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path(
        'v1/users/me/',
        MeViewSet.as_view({'get': 'me', 'patch': 'me'}),
        name="user_view_set"
    ),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SelfCreateUserView.as_view()),
    path('v1/auth/token/', get_token_view, name='get_token'),
]
