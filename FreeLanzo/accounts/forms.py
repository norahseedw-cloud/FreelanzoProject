from django import forms
from django.contrib.auth.models import User
from .models import FreelancerProfile,PortfolioProject


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    role = forms.ChoiceField(choices=[
        ('freelancer', 'Freelancer'),
        ('client', 'Client')
    ])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters")
        return password
    


class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = [
            'avatar',
            'job_title',
            'location',
            'category',
            'about',
            'skills',
            'hourly_rate',
            'availability',
            'languages'
        ]



class PortfolioProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = ['title', 'description', 'image', 'project_url']




