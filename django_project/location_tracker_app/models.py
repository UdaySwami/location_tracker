import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone
from .enums import UserRoles
from .user_ops.user_manager import UserManager


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    # Fields
    id = models.AutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.TextField(max_length=255, validators=[validate_email], unique=True)
    name = models.TextField(max_length=150)
    password = models.TextField(max_length=1024)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.IntegerField(default=UserRoles.Employee.value, choices=UserRoles.choices())
    last_login_at = models.DateTimeField(default=timezone.now, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Parent Model Fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # ('email',)

    # Manager
    objects = UserManager()

    # Functions
    def __str__(self):
        return self.email

    @staticmethod
    def as_user(json_object):
        u = User()
        u.__dict__.update(json_object)
        return u

    def get_short_name(self):
        pass

    def get_full_name(self):
        pass

    @property
    def is_staff(self):
        return self.is_superuser

    # Meta
    class Meta:
        db_table = 'Users'


class Location(models.Model):
    # Fields
    lat = models.FloatField()
    lng = models.FloatField()
    time = models.DateTimeField(default=timezone.now)
    next_location = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_first = models.BooleanField(default=False)

    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Locations'
