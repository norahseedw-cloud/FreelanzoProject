from django.shortcuts import render
from django.http import HttpRequest,HttpResponse

# Create your views here.

def projects_view(request:HttpRequest):

    return render(request, 'marketplace/projects.html')

def projects_detail_view(request:HttpRequest):

    return render(request, 'marketplace/project-detail.html')