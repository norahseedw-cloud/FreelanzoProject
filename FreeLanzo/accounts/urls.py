from django.urls import path
from . import views

app_name="accounts"

urlpatterns=[
    path('accounts/sign-up/', views.sign_up_view, name='sign_up_view'),
    path('accounts/sign-in/', views.sign_in_view, name='sign_in_view'),
    path('accounts/logout/', views.logout_view, name='logout_view'),
    path('accounts/terms-and-conditions/', views.terms_conditions_view, name="terms_conditions_view"),
    path('accounts/privacy-policy/', views.privacy_policy_view, name="privacy_policy_view"),

    path('freelancer/profile/', views.freelancer_profile_view, name='freelancer_profile'),
   path('client/profile/', views.client_profile_view, name='client_profile'),
path('client/<int:user_id>/', views.client_profile_view, name='client_profile_detail'),
    path('all/freelancer/', views.all_freelancer_view, name='all_freelancer'),
    path('freelancer/update/', views.update_freelancer_profile, name='update_freelancer_profile'),
    path('portfolio/add/', views.add_portfolio_project, name='add_portfolio_project'),
    path('portfolio/<int:project_id>/', views.portfolio_project_detail, name='portfolio_project_detail'),
    path('freelancer/<int:user_id>/', views.freelancer_profile_detail, name='freelancer_profile_detail'),
    path('portfolio/<int:project_id>/update/', views.update_portfolio_project, name='update_portfolio_project'),
    path('portfolio/<int:project_id>/delete/', views.delete_portfolio_project, name='delete_portfolio_project'),
    path('client/profile/update/', views.update_client_profile_view, name='update_client_profile'),
    path('project/create/', views.create_project_view, name='create_project'),
    path('projects/', views.all_projects_view, name='all_projects'),
    path('project/<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('project/update/<int:project_id>/', views.update_project_view, name='update_project'),
    path('freelancers/<int:freelancer_id>/favorite/',views.toggle_favorite_freelancer,name='toggle_favorite_freelancer'),
    path('favorites/freelancers/',views.favorite_freelancers_view,name='favorite_freelancers'),
]