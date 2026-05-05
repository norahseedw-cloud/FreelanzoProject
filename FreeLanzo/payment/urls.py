from django.urls import path
from . import views

app_name="payment"

urlpatterns = [
    path('pay/<int:project_id>/', views.create_checkout_session, name='pay_project'),
    path('success/', views.payment_success),
    path('cancel/', views.payment_cancel),
]