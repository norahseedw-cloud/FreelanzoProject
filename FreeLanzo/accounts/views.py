from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from .forms import SignUpForm,FreelancerProfileForm,PortfolioProjectForm,ClientProfileForm,ProjectForm
from .models import UserType, FreelancerProfile, ClientProfile,PortfolioProject, PortfolioProjectImage,PortfolioProjectImage,Project
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from marketplace.forms import ProposalForms, DeliveryForm
from marketplace.models import Proposal
from review.models import Review
from django.db.models import Avg, Sum

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


def all_freelancer_view(request):
    freelancers = FreelancerProfile.objects.all()

    category = request.GET.get('category')

    if category:
        freelancers = freelancers.filter(category=category)

    category_dict = dict(FreelancerProfile.CATEGORY_CHOICES)
    category_name = category_dict.get(category)

    return render(request, 'accounts/all-freelancer.html', {
        'freelancers': freelancers,
        'selected_category': category_name,
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
        'form': form,
        'profile':profile,
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
    can_review = False
    reviews = Review.objects.filter(reviewed_user=profile.user)
    average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    reviews_count = reviews.count()

    if request.user.is_authenticated and request.user != profile.user:

        has_relation = Proposal.objects.filter(
            project__client__user=request.user,
            freelancer=profile,
            status='accepted'
        ).exists() or Proposal.objects.filter(
            project__client__user=profile.user,
            freelancer__user=request.user,
            status='accepted'
        ).exists()

        if has_relation:
            can_review = True

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
        "can_review":can_review,
        "reviews":reviews,
        "average_rating": round(average_rating, 1),
    "reviews_count": reviews_count,
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



@login_required
def client_profile_view(request, user_id=None):

    if user_id:
        profile = get_object_or_404(ClientProfile, user__id=user_id)
    else:
        profile, created = ClientProfile.objects.get_or_create(user=request.user)

    projects = Project.objects.filter(client=profile).order_by('-created_at')

    total_spent = projects.filter(status='completed').aggregate(total=Sum('budget'))['total'] or 0

    freelancers_hired = Proposal.objects.filter(
        project__client=profile,
        status='accepted'
    ).values('freelancer').distinct().count()

    is_top_client = projects.count() >= 5

    return render(request, 'accounts/client-profile.html', {
        'profile': profile,
        'projects': projects,
        'total_spent': total_spent,
        'freelancers_hired': freelancers_hired,
        'is_top_client': is_top_client,
    })




@login_required
def update_client_profile_view(request):
    profile, created = ClientProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:client_profile')

    else:
        form = ClientProfileForm(instance=profile)

    return render(request, 'accounts/update-client-profile.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def create_project_view(request):
    profile, created = ClientProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.client = profile
            project.save()
            return redirect('accounts:client_profile')
    else:
        form = ProjectForm()

    return render(request, 'accounts/create-project.html', {
        'form': form
    })

def all_projects_view(request):
    projects = Project.objects.all().order_by('-created_at')

    category = request.GET.get('category')
    search = request.GET.get('search')

    if category:
        projects = projects.filter(category=category)

    if search:
        projects = projects.filter(title__icontains=search)

    category_dict = dict(FreelancerProfile.CATEGORY_CHOICES)
    selected_category_name = category_dict.get(category)

    return render(request, 'marketplace/projects.html', {
        'projects': projects,
        'categories': FreelancerProfile.CATEGORY_CHOICES,
        'selected_category': category,
        'selected_category_name': selected_category_name,
        'search': search,
    })

def project_detail_view(request: HttpRequest, project_id):

    project = get_object_or_404(Project, id=project_id)
    proposals = project.proposals.all()

    client_projects_count = Project.objects.filter(client=project.client).count()
    

    existing_proposal = None

    
    if request.user.is_authenticated and request.user.usertype.role == 'freelancer':
        existing_proposal = project.proposals.filter(freelancer=request.user.freelancerprofile).first()

   
    if request.method == "POST":

        
        if 'proposal_id' in request.POST:

            proposal_id = request.POST.get('proposal_id')
            action = request.POST.get('action')

            proposal = project.proposals.get(id=proposal_id)

           
            if request.user.is_authenticated and request.user == project.client.user:
                if action == 'accept':
                    proposal.status = 'accepted'
                    proposal.save()
                    

                    project.proposals.exclude(id=proposal.id).update(status='rejected')

                    project.status = 'in_progress'
                    project.save()
                    project.refresh_from_db()

                elif action == 'reject':
                    proposal.status = 'rejected'
                    proposal.save()
                    
            return redirect('accounts:project_detail', project_id=project.id)
        
        if 'accept_delivery' in request.POST:

            if request.user == project.client.user:

                project.status = 'completed'
                project.save()

            return redirect('accounts:project_detail', project_id=project.id)
        
        if 'delivery_submit' in request.POST:

   
            if not request.user.is_authenticated or request.user.usertype.role != 'freelancer':
                return redirect('main:home')

            proposal = project.proposals.filter(freelancer=request.user.freelancerprofile,status='accepted').first()

            if not proposal:
                return redirect('accounts:project_detail', project_id=project.id)

            form = DeliveryForm(request.POST, request.FILES)

            if form.is_valid():

               
                if not form.cleaned_data['file'] and not form.cleaned_data['url']:
                    return redirect('accounts:project_detail', project_id=project.id)

                
                if hasattr(proposal, 'delivery'):
                    return redirect('accounts:project_detail', project_id=project.id)

                delivery = form.save(commit=False)
                delivery.proposal = proposal
                delivery.save()

                
                
                project.save()

            return redirect('accounts:project_detail', project_id=project.id)

        
        if request.user.is_authenticated and request.user.usertype.role == 'freelancer':

            
            if existing_proposal:
                return redirect('accounts:project_detail', project_id=project.id)

            form = ProposalForms(request.POST)

            if form.is_valid():
                proposal = form.save(commit=False)
                proposal.project = project
                proposal.freelancer = request.user.freelancerprofile
                proposal.save()

                return redirect('accounts:project_detail', project_id=project.id)

    else:
        form = ProposalForms()

    accepted_proposal = project.proposals.filter(status='accepted').first()

   
    return render(request, 'marketplace/project-detail.html', {
        'project': project,
        'client_projects_count': client_projects_count,
        'form': form,
        'existing_proposal': existing_proposal,
        'proposals': proposals,
        'accepted_proposal':accepted_proposal
    })

