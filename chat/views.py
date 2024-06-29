from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import UserChats

def start_chat(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        model_name = request.POST.get('model')
        if username and model_name:
            UserChats.create(username)
            UserChats.add_session(username, model_name)
            return redirect('chat', model_name=model_name, username=username)
    return render(request, 'chat/landing.html')

def chat(request, model_name, username):
    user_chat = UserChats.get(username)
    return render(request, 'chat/chat.html', {'model_name': model_name, 'username': username})

def save_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        model_name = data.get('model')
        message_role = data.get('role')
        message_content = data.get('content')
        UserChats.add_message(username, model_name, message_role, message_content)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failure'})

def view_history(request, username):
    user_chat = UserChats.get(username)
    if user_chat:
        context = {'user_chat': user_chat}
    else:
        context = {'no_history': True, 'username': username}
    return render(request, 'chat/history.html', context)

def get_session_messages(request, username, model_name):
    user_chat = UserChats.get(username)
    if user_chat:
        for session in user_chat['sessions']:
            if session['model'] == model_name:
                return JsonResponse({'status': 'success', 'messages': session['messages']})
    return JsonResponse({'status': 'failure'})
