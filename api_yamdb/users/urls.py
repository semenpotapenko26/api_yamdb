from rest_framework import routers
from django.urls import path, include

from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
