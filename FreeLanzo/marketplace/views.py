from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from accounts.models import Project
from .forms import ProposalForms

# Create your views here.

def projects_view(request:HttpRequest):

    projects= Project.objects.all()
    

    return render(request, 'marketplace/projects.html',{"projects":projects})

