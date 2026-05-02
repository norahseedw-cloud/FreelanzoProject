from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from .forms import SignUpForm,FreelancerProfileForm,PortfolioProjectForm
from .models import UserType, FreelancerProfile, ClientProfile,PortfolioProject, PortfolioProjectImage,PortfolioProjectImage
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# Create your views here.

def sign_up_view(request):
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
            print(form.errors) 

    else:
        form = SignUpForm()

    return render(request, "accounts/sign-up.html", {"form": form})






# def sign_in_view(request:HttpRequest):
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


def sign_in_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("main:home")
        else:
            return render(request, "accounts/sign-in.html", {
                "error": "Username or password is incorrect"
            })

    return render(request, "accounts/sign-in.html")


def logout_view(request):
    logout(request)
    return redirect("main:home")


def terms_conditions_view(request:HttpRequest):
    
    return render(request, "accounts/terms-conditions.html")


def privacy_policy_view(request:HttpRequest):
    
    return render(request, "accounts/privacy-policy.html")


@login_required
def freelancer_profile_view(request):
    profile, created = FreelancerProfile.objects.get_or_create(user=request.user)
    projects = profile.portfolio_projects.all()

    similar_freelancers = FreelancerProfile.objects.filter(
        category=profile.category,
    ).exclude(user=request.user)[:3]

    return render(request, "accounts/freelancer-profile.html", {
        "profile": profile,
        "projects": projects,
        "similar_freelancers": similar_freelancers,
    })

def client_profile_view(request):
    return render(request, 'accounts/client-profile.html')


def all_freelancer_view(request):
    freelancers = FreelancerProfile.objects.all()

    return render(request, 'accounts/all-freelancer.html', {
        'freelancers': freelancers
    })


def portfolio_project_detail(request, project_id):
    project = get_object_or_404(PortfolioProject, id=project_id)

    return render(request, "accounts/portfolio-project-detail.html", {
        "project": project
    })

@login_required
def update_freelancer_profile(request):
    profile, created = FreelancerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = FreelancerProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('accounts:freelancer_profile')

    else:
        form = FreelancerProfileForm(instance=profile)

    return render(request, 'accounts/update-profile.html', {
        'form': form
    })


@login_required
def add_portfolio_project(request):
    profile, _ = FreelancerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PortfolioProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.freelancer = profile
            project.save()

            images = request.FILES.getlist('images')
            for img in images:
                PortfolioProjectImage.objects.create(
                    project=project,
                    image=img
                )

            return redirect("accounts:freelancer_profile")
    else:
        form = PortfolioProjectForm()

    return render(request, "accounts/add-portfolio-project.html", {"form": form})


def freelancer_profile_detail(request, user_id):
    profile = get_object_or_404(FreelancerProfile, user__id=user_id)
    projects = profile.portfolio_projects.all()

    if profile.category:
        similar_freelancers = FreelancerProfile.objects.filter(
            category=profile.category
        ).exclude(user=profile.user)[:3]
    else:
        similar_freelancers = FreelancerProfile.objects.exclude(
            user=profile.user
        )[:3]

    return render(request, "accounts/freelancer-profile.html", {
        "profile": profile,
        "projects": projects,
        "similar_freelancers": similar_freelancers,
    })


@login_required
def update_portfolio_project(request, project_id):
    project = get_object_or_404(PortfolioProject, id=project_id, freelancer__user=request.user)

    if request.method == "POST":
        form = PortfolioProjectForm(request.POST, request.FILES, instance=project)

        if form.is_valid():
            form.save()

            images = request.FILES.getlist("images")
            for img in images:
                PortfolioProjectImage.objects.create(project=project, image=img)

            return redirect("accounts:portfolio_project_detail", project_id=project.id)
    else:
        form = PortfolioProjectForm(instance=project)

    return render(request, "accounts/update-portfolio-project.html", {
        "form": form,
        "project": project
    })


@login_required
def delete_portfolio_project(request, project_id):

    project = get_object_or_404(PortfolioProject, id=project_id, freelancer__user=request.user)

    if request.method == "POST":
        project.delete()
        return redirect("accounts:freelancer_profile")

    return render(request, "accounts/delete-portfolio-project.html", {
        "project": project
    })


