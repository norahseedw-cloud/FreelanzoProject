from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review
from marketplace.models import Proposal
from django.contrib.auth.models import User

# Create your views here.



@login_required
def add_review_view(request:HttpRequest, user_id):
    if request.method == "POST":

        reviewed_user = get_object_or_404(User, id=user_id)

        if request.user == reviewed_user:
            return redirect('accounts:freelancer_profile_detail', user_id=user_id)

        has_relation = Proposal.objects.filter(
            project__client__user=request.user,
            freelancer__user=reviewed_user,
            status='accepted'
        ).exists() or Proposal.objects.filter(
            project__client__user=reviewed_user,
            freelancer__user=request.user,
            status='accepted'
        ).exists()

        if not has_relation:
            return redirect('accounts:freelancer_profile_detail', user_id=user_id)

       
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            reviewer=request.user,
            reviewed_user=reviewed_user,
            rating=rating,
            comment=comment
        )

        return redirect('accounts:freelancer_profile_detail', user_id=user_id)
    


@login_required
def delete_review(request:HttpResponse, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.reviewer != request.user:
        return redirect('accounts:freelancer_profile_detail', user_id=review.reviewed_user.id)

    review.delete()

    return redirect('accounts:freelancer_profile_detail', user_id=review.reviewed_user.id)
