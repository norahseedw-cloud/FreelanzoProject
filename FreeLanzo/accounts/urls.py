from django.urls import path
from . import views

app_name="accounts"

urlpatterns=[
    path('sign-up/', views.sign_up_view, name='sign_up_view'),
    path('sign-in/', views.sign_in_view, name='sign_in_view'),
    path('terms-and-conditions/', views.terms_conditions_view, name="terms_conditions_view"),
    path('privacy-policy/', views.privacy_policy_view, name="privacy_policy_view")
]