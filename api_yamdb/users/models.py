from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import USER_ROLE, USER


class User(AbstractUser):
    email = models.EmailField(
        'email address',
        blank=False,
        null=False,
        help_text='Required',
        unique=True
    )
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=150, choices=USER_ROLE, default=USER)
