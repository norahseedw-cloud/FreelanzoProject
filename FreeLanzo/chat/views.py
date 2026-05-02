from django.shortcuts import render
from django.http import HttpRequest,HttpResponse

# Create your views here.

def contact_view(request:HttpRequest):

    return render(request,'chat/contact-us.html')


def chat_view(request:HttpRequest):

    return render(request,'chat/chat.html')