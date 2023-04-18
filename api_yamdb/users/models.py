from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLE = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    email = models.EmailField(
        'email address',
        blank=False,
        null=False,
        help_text='Required',
        unique=True
    )
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=150, choices=USER_ROLE, default=USER)
