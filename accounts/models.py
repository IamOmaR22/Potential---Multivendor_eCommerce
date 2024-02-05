from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    BUYER = 'BUYER'
    SELLER = 'SELLER'

    USER_TYPE_CHOICES = (
        (BUYER, 'Buyer'),
        (SELLER, 'Seller')
    )

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True, blank=True)
    password = models.CharField(max_length=128)  # Assuming you'll handle hashing separately
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'user_type', 'first_name', 'last_name']

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        related_name='ecom_user_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        related_name='ecom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username
