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
    has_seen_profile_prompt = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Skill(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, related_name='skills')

    def __str__(self):
        return self.name

class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='freelancer_avatars/', blank=True, null=True, default='default-avatar.avif')
    job_title = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=150, blank=True)
    about = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name="freelancers")
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    availability = models.CharField(max_length=100, blank=True)
    languages = models.CharField(max_length=200, blank=True)
    experience = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to='client_avatars/', blank=True, null=True,default='default-avatar.avif')
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
    

class Project(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=8, decimal_places=2)
    skills = models.ManyToManyField(Skill, blank=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ('open', 'Open'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
        ),
        default='open'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class FavoriteFreelancer(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="favorite_freelancers")
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name="liked_by_clients")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'freelancer')

    def __str__(self):
        return f"{self.client.user.username} liked {self.freelancer.user.username}"