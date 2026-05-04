from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):

    class RatingChoices(models.IntegerChoices):
        STAR1 = 1, "One Star"
        STAR2 = 2, "Two Stars"
        STAR3 = 3, "Three Stars"
        STAR4 = 4, "Four Stars"
        STAR5 = 5, "Five Stars"

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')

    rating = models.SmallIntegerField(choices=RatingChoices.choices)
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
