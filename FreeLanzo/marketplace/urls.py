from django.urls import path
from . import views

app_name="marketplace"

urlpatterns=[
    path('projects/', views.projects_view, name='projects_view'),
    path('projects/detail/', views.projects_detail_view, name='projects_detail_view'),
]