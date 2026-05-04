from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from .forms import SignUpForm,FreelancerProfileForm,PortfolioProjectForm,ClientProfileForm,ProjectForm
from .models import UserType, FreelancerProfile, ClientProfile,PortfolioProject, PortfolioProjectImage,PortfolioProjectImage,Project,Category,FavoriteFreelancer
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from marketplace.forms import ProposalForms, DeliveryForm
from marketplace.models import Proposal
from review.models import Review
from django.db.models import Avg, Sum, Q


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

        skills__in=profile.skills.all()
    ).exclude(user=request.user).distinct()[:3]

    # category=(profile.category,).exclude(user=request.user)[:3]
    


    return render(request, "accounts/freelancer-profile.html", {
        "profile": profile,
        "projects": projects,
        "similar_freelancers": similar_freelancers,
    })


def all_freelancer_view(request):
    freelancers = FreelancerProfile.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    search = request.GET.get('search')
    min_rate = request.GET.get('min_rate')
    max_rate = request.GET.get('max_rate')
    sort = request.GET.get('sort')
    query = request.GET.get('q')

    if query:
        freelancers = freelancers.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(skills__name__icontains=query)
        ).distinct()


    if category_id and category_id.isdigit():
        freelancers = freelancers.filter(
            skills__categories__id=int(category_id)
        ).distinct()

    if search:
        freelancers = freelancers.filter(
            user__first_name__icontains=search
        ) | freelancers.filter(
            user__last_name__icontains=search
        ) | freelancers.filter(
            job_title__icontains=search
        ) | freelancers.filter(
            skills__name__icontains=search
        )
        freelancers = freelancers.distinct()

    if min_rate:
        freelancers = freelancers.filter(hourly_rate__gte=min_rate)

    if max_rate:
        freelancers = freelancers.filter(hourly_rate__lte=max_rate)

    if sort == "low":
        freelancers = freelancers.order_by("hourly_rate")
    elif sort == "high":
        freelancers = freelancers.order_by("-hourly_rate")

    return render(request, 'accounts/all-freelancer.html', {
        'freelancers': freelancers,
        'categories': categories,
        'selected_category': category_id,
        'search': search,
        'min_rate': min_rate,
        'max_rate': max_rate,
        'sort': sort,
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

    similar_freelancers = FreelancerProfile.objects.filter(
        skills__in=profile.skills.all()
    ).exclude(user=profile.user).distinct()[:3]

    is_liked = False

    if request.user.is_authenticated:
        client_profile = ClientProfile.objects.filter(user=request.user).first()

        if client_profile:
            is_liked = FavoriteFreelancer.objects.filter(
                client=client_profile,
                freelancer=profile
            ).exists()

    return render(request, "accounts/freelancer-profile.html",{
        "profile": profile,
        "projects": projects,
        "similar_freelancers": similar_freelancers,
        "is_liked": is_liked,

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

            skills = form.cleaned_data.get('skills')

            if skills:
                first_skill = skills.first()
                project.category = first_skill.categories.first()

            project.save()
            form.save_m2m()

            return redirect('accounts:client_profile')
        else:
            print(form.errors)

    else:
        form = ProjectForm()

    return render(request, 'accounts/create-project.html', {
        'form': form
    })



def all_projects_view(request):
    projects = Project.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    search = request.GET.get('search')
    min_budget = request.GET.get('min_budget')
    max_budget = request.GET.get('max_budget')
    sort = request.GET.get('sort')

    if category_id and category_id.isdigit():
        projects = projects.filter(category_id=int(category_id))
    else:
        category_id = None

    if search:
        projects = projects.filter(title__icontains=search)

    if min_budget:
        projects = projects.filter(budget__gte=min_budget)

    if max_budget:
        projects = projects.filter(budget__lte=max_budget)

    if sort == "low":
        projects = projects.order_by("budget")
    elif sort == "high":
        projects = projects.order_by("-budget")

    return render(request, 'marketplace/projects.html', {
        'projects': projects,
        'categories': categories,
        'selected_category': category_id,
        'search': search,
        'min_budget': min_budget,
        'max_budget': max_budget,
        'sort': sort,
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

@login_required
def update_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, client__user=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect('accounts:project_detail', project_id=project.id)

    else:
        form = ProjectForm(instance=project)

    return render(request, 'marketplace/update_project.html', {
        'form': form,
        'project': project,
    })

@login_required
def toggle_favorite_freelancer(request, freelancer_id):
    freelancer = get_object_or_404(FreelancerProfile, id=freelancer_id)

    client_profile = ClientProfile.objects.filter(user=request.user).first()

    if not client_profile:
        return redirect('accounts:all_freelancer')

    favorite, created = FavoriteFreelancer.objects.get_or_create(
        client=client_profile,
        freelancer=freelancer
    )

    if not created:
        favorite.delete()

    return redirect(request.META.get('HTTP_REFERER', 'accounts:all_freelancer'))


@login_required
def favorite_freelancers_view(request):
    client_profile = ClientProfile.objects.filter(user=request.user).first()

    if not client_profile:
        return redirect('accounts:all_freelancer')

    favorites = FavoriteFreelancer.objects.filter(
        client=client_profile
    ).select_related('freelancer__user')

    return render(request, 'accounts/favorite_freelancers.html', {
        'favorites': favorites,
    })

    


