from __future__ import unicode_literals
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _add_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        :param email: string
        :param password: string
        :param extra_fields: other fields
        :return: object
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._add_user(email, password, **extra_fields)

