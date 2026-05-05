import stripe
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from accounts.models import Project
from django.contrib import messages


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request:HttpRequest, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.client:
        messages.error(request, "You are not allowed to pay for this project.", "alert-danger")
        return redirect('accounts:project_detail', project_id=project.id)
    
    if project.status == 'completed':
        messages.warning(request, "This project is already completed." , "alert-warning")
        return redirect('accounts:project_detail', project_id=project.id)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': project.title,
                    },
                    'unit_amount': int(project.budget * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/payment/success/'),
            cancel_url=request.build_absolute_uri('/payment/cancel/'),
            metadata={
                "project_id": project.id
            }
        )

        return redirect(session.url)
    except Exception as e:
        messages.error(request, "Payment session failed. Please try again." , "alert-danger")
        return redirect('accounts:project_detail', project_id=project.id)


def payment_success(request:HttpRequest):
    return HttpResponse("Payment Successful ✅")

def payment_cancel(request:HttpRequest):
    return HttpResponse("Payment Cancelled ❌")