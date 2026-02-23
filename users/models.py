from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[('customer', 'Customer'), ('admin', 'Admin')], default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'  # idu user login aguvaga email beku , not username
    REQUIRED_FIELDS = ['username', 'phone_number'] # idu super user create maduvaga beku iverdu

    def __str__(self):
        return self.email

