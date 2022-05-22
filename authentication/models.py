from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password=None, **extra_fields):
        if username is None:
            msg = _("User should have a username")
            raise TypeError(msg)
        if email is None:
            msg = _("User should have an email")
            raise TypeError(msg)

        user = self.model(
            username=username, email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            msg = _("Superuser must have is_staff=True")
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = _("Superuser must have is_superuser=True")
            raise ValueError(msg)
        if extra_fields.get("is_admin") is not True:
            msg = _("Superuser must have is_admin=True")
            raise ValueError(msg)

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=50, unique=True, db_index=True, validators=[username_validator]
    )
    email = models.EmailField(max_length=250, unique=True, db_index=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def token(self):
        _token = RefreshToken.for_user(self)
        return {
            "refresh": str(_token),
            "access": str(_token.access_token),
        }

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
