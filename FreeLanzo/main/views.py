from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from accounts.models import FreelancerProfile, Project,Category
from review.models import Review
from django.db.models import Count , Avg

# Create your views here.

def home_view(request:HttpRequest):
    freelancers_count = FreelancerProfile.objects.count()
    projects_count = Project.objects.count()
    categories_count = Category.objects.count()
    categories = Category.objects.annotate(freelancers_count=Count('skills__freelancers', distinct=True))
    avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
    satisfaction = int((avg_rating / 5) * 100)
    top_freelancers = FreelancerProfile.objects.annotate(avg_rating=Avg('user__received_reviews__rating')).order_by('-avg_rating')[:3]
    completed_projects = Project.objects.filter(status='completed').count()
    testimonials = Review.objects.select_related('reviewer','reviewer__clientprofile').order_by('-created_at')[:3]


    return render(request,'main/home.html' ,{
        'freelancers_count': freelancers_count,
        'projects_count': projects_count,
        'categories_count': categories_count,
        'categories': categories,
        'satisfaction': satisfaction,
        'top_freelancers': top_freelancers,
        'completed_projects': completed_projects,
        'testimonials': testimonials,
    })


def about_view(request:HttpRequest):


    return render(request,'main/about-us.html')


def mode_view(request, mode):
    response = redirect(request.GET.get('next', '/'))

    current_mode = request.COOKIES.get('mode', 'light')

    if mode == "toggle":
        new_mode = "dark" if current_mode == "light" else "light"
    else:
        new_mode = mode

    response.set_cookie('mode', new_mode, max_age=60*60*24*30)

    return response