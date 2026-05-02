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
    avatar = models.ImageField(upload_to='freelancer_avatars/', blank=True, null=True)
    job_title = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=150, blank=True)
    about = models.TextField(blank=True)
    skills = models.CharField(max_length=300, blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    availability = models.CharField(max_length=100, blank=True)
    languages = models.CharField(max_length=200, blank=True)

    CATEGORY_CHOICES = (
        ('graphics_design', 'Graphics & Design'),
        ('programming_tech', 'Programming & Tech'),
        ('digital_marketing', 'Digital Marketing'),
        ('video_animation', 'Video & Animation'),
        ('writing_translation', 'Writing & Translation'),
        ('business', 'Business'),
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)

    def __str__(self):
        return self.user.username



class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to='client_avatars/', blank=True, null=True)
    company_name = models.CharField(max_length=150, blank=True)
    job_title = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=150, blank=True)
    about = models.TextField(blank=True)
    preferred_categories = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.user.username


class PortfolioProject(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name="portfolio_projects")
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="portfolio_images/", blank=True, null=True)
    project_url = models.URLField(blank=True)

    def __str__(self):
        return self.title
    
class PortfolioProjectImage(models.Model):
    project = models.ForeignKey(PortfolioProject, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="portfolio_images/")

    def __str__(self):
        return f"Image for {self.project.title}"