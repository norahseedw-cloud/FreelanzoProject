from django.shortcuts import render

def payment_view(request):
    return render(request, 'payment/payment.html')

# Create your views here.
