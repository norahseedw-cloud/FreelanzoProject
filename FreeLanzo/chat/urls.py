from django.urls import path
from . import views

app_name="chat"

urlpatterns=[
    path('contact/us', views.contact_view, name="contact_view"),
    path('chat', views.chat_view, name="chat_view"),
]