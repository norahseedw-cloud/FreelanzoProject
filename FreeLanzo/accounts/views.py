from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from .forms import SignUpForm
from .models import UserType, FreelancerProfile, ClientProfile
from django.contrib.auth import login,authenticate,logout


# Create your views here.

def sign_up_view(request:HttpRequest):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            role = form.cleaned_data['role']

            UserType.objects.create(user=user, role=role)

            if role == "freelancer":
                FreelancerProfile.objects.create(user=user)
            else:
                ClientProfile.objects.create(user=user)

            return redirect("accounts:sign_in_view")

    else:
        form = SignUpForm()

    return render(request, "accounts/sign-up.html", {"form": form}) 


def sign_in_view(request:HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            request.session['show_complete_profile'] = True

            return redirect("main:home")

        else:
            print("Login failed")

    return render(request, "accounts/sign-in.html")

def logout_view(request:HttpRequest):
    logout(request)
    return redirect("accounts:sign_in_view")

def terms_conditions_view(request:HttpRequest):
    
    return render(request, "accounts/terms-conditions.html")

def privacy_policy_view(request:HttpRequest):
    
    return render(request, "accounts/privacy-policy.html")


def freelancer_profile_view(request):
    return render(request, 'accounts/freelancer-profile.html')

def client_profile_view(request):
    return render(request, 'accounts/client-profile.html')

def all_freelancer_view(request):
    return render(request, 'accounts/all-freelancer.html')
