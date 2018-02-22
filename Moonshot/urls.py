"""Moonshot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from Moonshot.views import *
from chat.views import *
# from Moonshot.chat.views import call

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', register, {'template_name': 'register.html'}, name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}),
    url(r'^$', home, name='HOME_PAGE'),
    url(r'^post/$', Post, name='post'),
    url(r'^messages/$', Messages, name='messages'),
    url(r'^home/(?P<guide_name>\w+)/$', Home, name='home'),
    url(r'^guides/$', Guide, name='guide'),
    url(r'^event/$', event_page, name='event'),
    url(r'^experience/$', experience_list, name='experience'),
    url(r'^upvote_experience/$', upvote_experience),
    url(r'^going_event/$', going_event),
    url(r'^guiding_event/$', guide_event),

]
