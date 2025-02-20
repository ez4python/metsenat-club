from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.admins.managers import CustomUserManager
from apps.shared.validators import validate_phone_number


# Create your models here.
class Admin(AbstractUser):
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number], unique=True)

    USERNAME_FIELD = 'username'  # username is used for login and to create superuser
    REQUIRED_FIELDS = []  # there are no other required fields when creating a superuser

    # excluded fields
    email = None
    groups = None
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"
        db_table = 'admins'

    def __str__(self):
        return self.get_full_name()
