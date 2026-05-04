from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name="accounts"

urlpatterns=[
    path('sign-up/', views.sign_up_view, name='sign_up_view'),
    path('sign-in/', views.sign_in_view, name='sign_in_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('terms-and-conditions/', views.terms_conditions_view, name="terms_conditions_view"),
    path('privacy-policy/', views.privacy_policy_view, name="privacy_policy_view"),
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
    path('freelancers/<int:freelancer_id>/favorite/',views.toggle_favorite_freelancer,name='toggle_favorite_freelancer'),
    path('favorites/freelancers/',views.favorite_freelancers_view,name='favorite_freelancers'),
    path('skip-complete-profile/', views.skip_complete_profile, name='skip_complete_profile'),
    path("password-reset/",auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html",email_template_name="accounts/password_reset_email.html",subject_template_name="accounts/password_reset_subject.txt",success_url="/accounts/password-reset/done/"),name="password_reset"),
    path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html",success_url="/accounts/password-reset-complete/"),name="password_reset_confirm"),
    path("password-reset-complete/",auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),name="password_reset_complete"),
]