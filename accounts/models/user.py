from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rules import always_allow, is_authenticated, is_staff
from rules.contrib.models import RulesModelBase, RulesModelMixin

from accounts.managers import CustomUserManager
from accounts.rules import is_owner


class User(
    RulesModelMixin,
    AbstractBaseUser,
    PermissionsMixin,
    metaclass=RulesModelBase,
):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        rules_permissions = {
            "add": always_allow,
            "view": is_authenticated,
            "change": is_owner | is_staff,
            "delete": is_staff,
        }

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
