from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from .models import EXPERIENCE
from django.template import loader

from database.functions import *
from Moonshot.forms import UserRegistrationForm

def home(request):
    return render(request, 'home.html')


def register(request, template_name):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            name = userObj['name']
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                create_user(user, name)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, template_name, {'form' : form})



def experience_list(request):
    all_experiences=EXPERIENCE.objects.all()
    template=loader.get_template('experience.html')
    context={
        'all_experiences': all_experiences,
    }
    return render(request, "experience.html", context)
