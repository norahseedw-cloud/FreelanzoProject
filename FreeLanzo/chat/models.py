from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Conversation(models.Model):
    user1= models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_as_user1')
    user2= models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    


class Message(models.Model):
    conversation= models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender= models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
    
