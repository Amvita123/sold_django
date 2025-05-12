import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from .managers import UserManager
from preferences.models import Preference

class User(Preference, AbstractBaseUser, PermissionsMixin):
    ACCOUNT_STATUS = (
        ('disabled', 'Disabled'),
        ('enabled', 'Enabled'),
        ('suspended', 'Suspended'),
        ('deleted', 'Deleted')
    )

    AUTH_PROVIDER = (
        ('email', 'Email'),
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('apple', 'Apple')
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
        ('undisclosed', 'Undisclosed')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=120, null=True, blank=True)
    phone_number = models.CharField(max_length=10, default="",null=False, blank=True)

    auth_provider = models.CharField(max_length=15, choices=AUTH_PROVIDER, null=True, blank=True)
    account_status = models.CharField(max_length=15, choices=ACCOUNT_STATUS, default="enabled", null=False, blank=False)

    is_email_verified = models.BooleanField(default=False)
    is_number_verified = models.BooleanField(default=False)

    about = models.CharField(max_length=200, default="", blank=True)
    profile_pic = models.URLField(default="https://eu.ui-avatars.com/api/?name=Amit+Kumar&size=450", blank=True, null=False)

    country = models.CharField(max_length=120, default="IN", blank=True)

    sex = models.CharField(max_length=50, choices=GENDER_CHOICES, default="undisclosed")
    address = models.TextField(max_length=200, default="", blank=True)
    nickname = models.CharField(max_length=120, default="", blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.fullname or self.email
