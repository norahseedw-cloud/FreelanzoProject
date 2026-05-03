from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from .models import Conversation, Message
from django.db.models import Q, Max, Count

# Create your views here.

def contact_view(request:HttpRequest):

    return render(request,'chat/contact-us.html')


def chat_view(request:HttpRequest, conversation_id=None):

    if conversation_id:
        conversation = Conversation.objects.get(pk=conversation_id)
        Message.objects.filter(conversation=conversation,is_read=False).exclude(sender=request.user).update(is_read=True)
        messages = Message.objects.filter(conversation=conversation).order_by('created_at')
    else:
        conversation = None
        messages = []

    if request.method=="POST":
        Message.objects.create(
            conversation=conversation,
            sender= request.user,
            content=request.POST["content"]
        )
        return redirect ("chat:chat_view", conversation_id)
    
    conversations=Conversation.objects.filter(Q(user1=request.user)| Q(user2=request.user)).annotate(
    unread_count=Count(
    'message',
    filter=Q(message__is_read=False) & ~Q(message__sender=request.user)),
    last_message_time=Max('message__created_at')).order_by('-last_message_time')

    return render(request,'chat/chat.html', {
        "conversation": conversation,
        "messages":messages,
        "conversations":conversations,
        })

def delete_conversation(request, conversation_id):
    conversation = Conversation.objects.get(pk=conversation_id)

    if request.user == conversation.user1 or request.user == conversation.user2:
        conversation.delete()

    return redirect('chat:chat_view')