from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHISES = (
        ('admin', 'Admin'),
        ('cliente', 'Cliente')
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'last_name', 'phone_number', 'role']
    
    role = models.CharField(max_length=10, choices=ROLE_CHISES)
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.username} - {self.role}"