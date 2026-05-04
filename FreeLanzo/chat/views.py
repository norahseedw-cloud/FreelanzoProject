from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from .models import Conversation, Message
from django.db.models import Q, Max, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required(login_url='accounts:sign_in_view')
def contact_view(request:HttpRequest):
    if request.method == "POST":
        text = request.POST.get("message")

        if not text or not text.strip():
            messages.error(request, "Message cannot be empty.", "alert-danger")
            return render(request, 'chat/contact-us.html')

        admin_user = User.objects.filter(is_superuser=True).first()

        if not admin_user:
            messages.error(request, "No admin available. Please try again later.","alert-danger")
            return render(request, 'chat/contact-us.html')

        conversation = Conversation.objects.filter(user1=request.user,user2=admin_user).first() or Conversation.objects.filter(user1=admin_user,user2=request.user).first()

        if not conversation:conversation = Conversation.objects.create(user1=request.user,user2=admin_user)
       
        Message.objects.create(conversation=conversation,sender=request.user,content=text)

        return redirect('chat:chat_view', conversation.id)

    return render(request,'chat/contact-us.html')



@login_required
def chat_view(request: HttpRequest, conversation_id=None):

    if conversation_id:
        conversation = Conversation.objects.filter(pk=conversation_id).first()

        
        if not conversation:
            messages.error(request, "Conversation not found.", "alert-danger")
            return redirect("main:home")

        
        if request.user not in [conversation.user1, conversation.user2]:
            messages.error(request, "You are not allowed to access this conversation.", "alert-danger")
            return redirect("main:home")

        Message.objects.filter(
            conversation=conversation,
            is_read=False
        ).exclude(sender=request.user).update(is_read=True)

        chat_messages = Message.objects.filter(
            conversation=conversation
        ).order_by('created_at')

    else:
        conversation = None
        chat_messages = []

    if request.method == "POST":

       
        if not conversation:
            messages.error(request, "No conversation selected.","alert-danger")
            return redirect("chat:chat_view")

        text = request.POST.get("content")

        
        if not text or not text.strip():
            messages.warning(request, "Message cannot be empty.", "alert-warning")
            return redirect("chat:chat_view", conversation_id)

        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=text
        )

        return redirect("chat:chat_view", conversation_id)

    conversations = Conversation.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).annotate(
        unread_count=Count(
            'message',
            filter=Q(message__is_read=False) & ~Q(message__sender=request.user)
        ),
        last_message_time=Max('message__created_at')
    ).order_by('-last_message_time')

    return render(request, 'chat/chat.html', {
        "conversation": conversation,
        "chat_messages": chat_messages,
        "conversations": conversations,
    })





@login_required
def delete_conversation(request: HttpResponse, conversation_id):
    conversation = Conversation.objects.filter(pk=conversation_id).first()

    
    if not conversation:
        messages.error(request, "Conversation not found.", "alert-danger")
        return redirect('chat:chat_view')

    
    if request.user != conversation.user1 and request.user != conversation.user2:
        messages.error(request, "You are not allowed to delete this conversation.", "alert-danger")
        return redirect('chat:chat_view')

    conversation.delete()
    messages.success(request, "Conversation deleted successfully.", "alert-success")

    return redirect('chat:chat_view')

@login_required
def start_chat(request, user_id):
    other_user = User.objects.filter(id=user_id).first()

    if not other_user:
        messages.error(request, "User not found.", "alert-danger")
        return redirect('main:home')

    
    if request.user == other_user:
        messages.warning(request, "You cannot start a chat with yourself.", "alert-warning")
        return redirect('main:home')

    conversation = Conversation.objects.filter(
        Q(user1=request.user, user2=other_user) |
        Q(user1=other_user, user2=request.user)
    ).first()

    if not conversation:
        conversation = Conversation.objects.create(
            user1=request.user,
            user2=other_user
        )
        messages.success(request, "Chat started successfully.", "alert-success")

    return redirect('chat:chat_view', conversation.id)