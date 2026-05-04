from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review
from marketplace.models import Proposal
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.



@login_required
def add_review_view(request:HttpRequest, user_id):
    if request.method == "POST":

        reviewed_user = get_object_or_404(User, id=user_id)

        if request.user == reviewed_user:
            messages.error(request, "You cannot review yourself." , "alert-danger")
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
            messages.error(request, "You can only review users you have worked with.", "alert-danger")
            return redirect('accounts:freelancer_profile_detail', user_id=user_id)

       
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not rating or not str(rating).isdigit() or int(rating) not in [1,2,3,4,5]:
            messages.error(request, "Please select a valid rating." , "alert-danger")
            return redirect('accounts:freelancer_profile_detail', user_id=user_id)
        
        if not comment or not comment.strip():
            messages.error(request, "Comment cannot be empty.", "alert-danger")
            return redirect('accounts:freelancer_profile_detail', user_id=user_id)

        Review.objects.create(
            reviewer=request.user,
            reviewed_user=reviewed_user,
            rating=rating,
            comment=comment
        )

        messages.success(request, "Your review has been submitted successfully.", "alert-success")

        return redirect('accounts:freelancer_profile_detail', user_id=user_id)
    


@login_required
def delete_review(request:HttpResponse, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.reviewer != request.user:
        messages.error(request, "You are not allowed to delete this review.", "alert-danger")
        return redirect('accounts:freelancer_profile_detail', user_id=review.reviewed_user.id)

    review.delete()
    messages.success(request, "Review deleted successfully.", "alert-success")

    return redirect('accounts:freelancer_profile_detail', user_id=review.reviewed_user.id)
