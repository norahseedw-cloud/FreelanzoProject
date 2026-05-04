from django import forms
from .models import Proposal,Delivery

class ProposalForms(forms.ModelForm):
    class Meta:
        model=Proposal
        fields=['cover_letter','price','duration']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['file', 'url', 'message']