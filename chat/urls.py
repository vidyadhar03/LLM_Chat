from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_chat, name='start_chat'),
    path('chat/<str:model_name>/<str:username>/', views.chat, name='chat'),
    path('save_message/', views.save_message, name='save_message'),
    path('history/<str:username>/', views.view_history, name='view_history'),
    path('get_session_messages/<str:username>/<str:model_name>/', views.get_session_messages, name='get_session_messages'),
]
