from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse

from database.functions import *
from Moonshot.models import LIVE_CHAT,USER, GUIDE_AVAILABLE


def chat(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    receiver_username = request.GET['receiver']
    sender_username = request.user.username
    receiver = get_user(receiver_username)

    c = get_all_messages(sender_username, receiver_username)
    return render(request, "ChatAppPage.html", {'home': 'active', 'chat': c, 'receiver_name': receiver.NAME,
                                                'sender':sender_username, 'receiver':receiver_username})


def post_message(request):
    if request.method == "POST":
        message = request.POST.get('msgbox', None)
        receiver = request.POST.get('receiver', None)
        sender = request.POST.get('sender', None)

        if message != '':
            store_message(sender, receiver, message)
        return JsonResponse({'msg': message})
    else:
        return HttpResponse('Request must be POST.')


def chat_refresh(request):
    receiver_username = request.GET['receiver']
    sender_username = request.GET['sender']
    c = get_all_messages(sender_username, receiver_username)
    return render(request, 'messages.html', {'chat': c, 'sender':sender_username, 'receiver':receiver_username})
