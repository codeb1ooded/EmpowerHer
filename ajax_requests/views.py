# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import *

from database.functions import *


def upvote_experience(request):
    '''if not request.user.is_authenticated:
        print "not authenticate"
        return redirect('/login')'''

    experience_id = request.GET['experience_id']
    newstate = request.GET['state']
    username = request.GET['username']
    upvote = True

    if newstate == "True":
        upvote = True
    else:
        upvote = False

    upvotes = up_down_vote_experience(username, experience_id, upvote)
    return HttpResponse(upvotes)


def upvote_answer(request):
    answer_id = request.GET['answer_id']
    newstate = request.GET['state']
    username = request.GET['username']
    upvote = True

    if newstate == "True":
        upvote = True
    else:
        upvote = False

    upvotes = up_down_vote_answer(username, answer_id, upvote)
    return HttpResponse(upvotes)


def going_event(request):
    '''if not request.user.is_authenticated:
        print "not authenticate"
        return redirect('/login')'''

    event_id = request.GET['event_id']
    newstate = request.GET['state']
    username = request.GET['username']
    going = True

    if newstate == "True":
        going = True
    else:
        going = False

    return HttpResponse(user_going(username, event_id, going))


def guide_event(request):
    '''if not request.user.is_authenticated:
        print "not authenticate"
        return redirect('/login')'''

    event_id = request.GET['event_id']
    newstate = request.GET['state']
    username = request.GET['username']
    guiding = True

    if newstate == "True":
        guiding = True
    else:
        guiding = False

    return HttpResponse(user_guiding(username, event_id, guiding))


def submit_answer_view(request):
    answer_id = request.GET['answer_id']
    question_id = request.GET['question_id']
    answer = request.GET['answer']

    is_logged_in = request.user.is_authenticated
    username = None
    if is_logged_in:
        username = request.user.username

    if answer_id == '-1':
        answer_id = submit_answer(question_id, answer, username)
    else:
        answer_id = update_answer(question_id, answer_id, answer, username)
    return HttpResponse(answer_id)


def submit_experience_view(request):
    experience_id = request.GET['experience_id']
    event_id = request.GET['event_id']
    experience = request.GET['experience']

    is_logged_in = request.user.is_authenticated
    username = None
    if is_logged_in:
        username = request.user.username

    if experience_id == '-1':
        experience_id = submit_experience(event_id, experience, username)
    else:
        experience_id = update_experience(experience_id, event_id, experience, username)
    return HttpResponse(experience_id)

def submit_question_view(request):
    event_id = request.GET['event_id']
    question = request.GET['question']

    is_logged_in = request.user.is_authenticated
    username = None
    if is_logged_in:
        username = request.user.username
    question_id = submit_question(event_id, question, username)
    return HttpResponse(question_id)
