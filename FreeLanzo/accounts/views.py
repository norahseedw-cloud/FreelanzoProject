from django.shortcuts import render
from django.http import HttpRequest,HttpResponse

# Create your views here.

def sign_up_view(request:HttpRequest):
    
    return render(request, "accounts/sign-up.html")


def sign_in_view(request:HttpRequest):
    
    return render(request, "accounts/sign-in.html")

def terms_conditions_view(request:HttpRequest):
    
    return render(request, "accounts/terms-conditions.html")

def privacy_policy_view(request:HttpRequest):
    
    return render(request, "accounts/privacy-policy.html")
