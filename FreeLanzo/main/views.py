from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse

# Create your views here.

def home_view(request:HttpRequest):


    return render(request,'main/home.html')


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