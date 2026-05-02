from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserType(models.Model):
    ROLE_CHOICES = (
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)