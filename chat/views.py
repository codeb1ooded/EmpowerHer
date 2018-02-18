from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from chat import settings
from django.shortcuts import get_object_or_404
from Moonshot.models import LIVE_CHAT,USER, GUIDE_AVAILABLE


def Home(request):
    c = LIVE_CHAT.objects.all()
    return render(request, "ChatAppPage.html", {'home': 'active', 'chat': c})

def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        # print request.user
        my_p = get_object_or_404(USER, USER_REF = request.user)
        print "="*30
        c = LIVE_CHAT(SENDER_KEY=my_p, MESSAGE=msg)
        print c.SENDER_KEY
        if msg != '':
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.SENDER_KEY.NAME })
    else:
        return HttpResponse('Request must be POST.')

def Messages(request):
    c = LIVE_CHAT.objects.all()
    return render(request, 'messages.html', {'chat': c})

def Guide(request):
    c = GUIDE_AVAILABLE.objects.all()
    return render(request, "All_guide.html", {'home': 'active', 'chat': c})
