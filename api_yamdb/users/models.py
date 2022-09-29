from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from .validators import UsernameValidator

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'User'),
    (MODERATOR, 'Moderator'),
    (ADMIN, 'Admin')
]


class UserManager(UserManager):

    def create_superuser(self, **extra_fields):
        extra_fields['role'] = ADMIN
        extra_fields['is_superuser'] = 1
        extra_fields['is_staff'] = 1
        return super()._create_user(**extra_fields)


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UsernameValidator('me'), ]
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    bio = models.TextField(
        'Bio',
        blank=True,
    )
    role = models.CharField(
        'Role',
        choices=ROLES,
        default=USER,
        max_length=300
    )

    @property
    def is_moderator(self):
        return self.role == MODERATOR or self.is_staff

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    objects = UserManager()
