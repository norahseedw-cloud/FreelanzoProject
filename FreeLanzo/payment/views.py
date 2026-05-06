from django.shortcuts import render
import stripe
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from accounts.models import Project  

def payment_view(request):
    return render(request, 'payment/payment.html')

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request:HttpRequest, project_id):
    project = get_object_or_404(Project, id=project_id)

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
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cancel/',
        metadata={
            "project_id": project.id
        }
    )

    return redirect(session.url)
