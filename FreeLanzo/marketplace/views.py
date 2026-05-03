from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from accounts.models import Project

# Create your views here.

def projects_view(request:HttpRequest):

    projects= Project.objects.all()

    return render(request, 'marketplace/projects.html',{"projects":projects})

def projects_detail_view(request:HttpRequest):

    return render(request, 'marketplace/project-detail.html')