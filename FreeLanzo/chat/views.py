from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from .models import Conversation, Message
from django.db.models import Q, Max, Count
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='accounts:sign_in_view')
def contact_view(request:HttpRequest):
    if request.method == "POST":
        text = request.POST.get("message")

        admin_user = User.objects.filter(is_superuser=True).first()

       
        conversation = Conversation.objects.filter(user1=request.user,user2=admin_user).first() or Conversation.objects.filter(user1=admin_user,user2=request.user).first()

       
        if not conversation:conversation = Conversation.objects.create(user1=request.user,user2=admin_user)

       
        Message.objects.create(conversation=conversation,sender=request.user,content=text)

        return redirect('chat:chat_view', conversation.id)

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



@login_required
def delete_conversation(request:HttpResponse, conversation_id):
    conversation = Conversation.objects.get(pk=conversation_id)

    if request.user == conversation.user1 or request.user == conversation.user2:
        conversation.delete()

    return redirect('chat:chat_view')

def start_chat(request, user_id):
    other_user = User.objects.get(id=user_id)

    conversation = Conversation.objects.filter(
        Q(user1=request.user, user2=other_user) |
        Q(user1=other_user, user2=request.user)
    ).first()

    if not conversation:
        conversation = Conversation.objects.create(
            user1=request.user,
            user2=other_user
        )

    return redirect('chat:chat_view', conversation.id)