from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseUserManager(models.Manager):
    @classmethod
    def normalize_username(cls, phone):
        """
        Normalize the username by lowercasing it.
        """
        phone = phone or ""
        if len(phone) < 11:
            raise ValueError(_('phone number must have at least 11 characters'))
        return phone.lower()

    def get_by_natural_key(self, phone):
        return self.get(**{self.model.USERNAME_FIELD: phone})


class UserManager(BaseUserManager):

    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given phone and password.
        """
        if not phone:
            raise ValueError(_('Users must have a username'))

        user = self.model(
            phone=self.normalize_username(phone)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given phone and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


