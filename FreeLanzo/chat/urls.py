from django.urls import path
from . import views

app_name="chat"

urlpatterns=[
    path('contact/us', views.contact_view, name="contact_view"),
    path('chat/', views.chat_view, name="chat_view"),
    path('chat/<int:conversation_id>/', views.chat_view, name="chat_view"),
    path('chat/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('chat/start/<int:user_id>/', views.start_chat, name='start_chat')
]