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
from ajax_requests.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home),

    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}),
    url(r'^signinup/$', sign_in_up_view),
    url(r'^signin/$', sign_in_view),
    url(r'^signup/$', sign_up_view),

    url(r'^create_event/$', create_event_view),
    url(r'^update_event/$', update_event_view),

    url(r'^event/$', event_page),
    url(r'^experience/$', experience_list, name='experience'),
    url(r'^question/$', answers_for_question, name='answers'),

    url(r'^upvote_experience/$', upvote_experience),
    url(r'^upvote_answer/$', upvote_answer),
    url(r'^going_event/$', going_event),
    url(r'^guiding_event/$', guide_event),
    url(r'^submit_question/$', submit_question_view),
    url(r'^submit_answer/$', submit_answer_view),
    url(r'^submit_experience/$', submit_experience_view),

]
