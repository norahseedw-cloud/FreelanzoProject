from django.db import models
from accounts.models import Project, FreelancerProfile

# Create your models here.

class Proposal(models.Model):

    class TextChoicesStatus(models.TextChoices):
        PENDING= 'pending', 'pending'
        ACCEPTED= 'accepted', 'accepted'
        REJECTED= 'rejected', 'rejected'

    freelancer=models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='proposals')
    cover_letter=models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration=models.IntegerField()
    status = models.CharField(max_length=10, choices=TextChoicesStatus.choices,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)


class Delivery(models.Model):
    proposal = models.OneToOneField(Proposal, on_delete=models.CASCADE)
    file = models.FileField(upload_to='deliveries/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
