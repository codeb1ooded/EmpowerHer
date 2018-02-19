from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import *
from django.contrib.auth.models import User
from django.http import *
import json

from database.functions import *
from Moonshot.forms import UserRegistrationForm

def home(request):
    return render(request, 'home.html')


def event_page(request):
    if not request.method == 'GET' or not 'event_id' in request.GET:       # URL is not valid
        return HttpResponseBadRequest()
    event_id = request.GET['event_id']

    is_logged_in = request.user.is_authenticated
    is_guide = False
    is_going = False
    username = None
    if is_logged_in:
        username = request.user.username
        print username
        is_guide = is_user_guide(username, event_id)
        is_going = is_user_going(username, event_id)
    event = get_event_details(event_id)
    if event is None:           # No such event exist in database
        raise Http404
    guides = get_all_guides(event_id)
    experiences = get_all_experiences(event_id)
    questions = get_all_questions(event_id)

    guide_array = []
    rn = len(guides)
    if len(guides) > 5:
        rn = 5
    for i in range(0, rn):
        guide = {}
        guide['guide_name'] = guides[i].USER_KEY.NAME
        guide['username'] = guides[i].USER_KEY.USER_REF.username
        guide['reputation'] = guides[i].USER_KEY.EXPERIENCE_UPVOTE + guides[i].USER_KEY.ANSWER_UPVOTE + guides[i].USER_KEY.GUIDE_UPVOTE + guides[i].USER_KEY.NUM_QUESTION_ASKED
        guide_array.append(guide)

    experience_array = []
    rn = len(experiences)
    if len(experiences) > 5:
        rn = 5
    for i in range(0, rn):
        experience = {}
        experience['experience'] = experiences[i].EXPERIENCE
        experience['timestamp'] = experiences[i].TIMESTAMP
        experience['username'] = experiences[i].USER_KEY.USER_REF.username
        experience['name'] = experiences[i].USER_KEY.NAME
        experience['upvotes'] = experiences[i].NUM_UPVOTES
        if is_logged_in:
            experience['is_upvoted'] = is_user_upvoted_experience(username, experiences[i].EXPERIENCE_ID)
        else:
            experience['is_upvoted'] = false
        experience_array.append(experience)

    question_array = []
    rn = len(questions)
    if len(questions) > 5:
        rn = 5
    for i in range(0, rn):
        question = {}
        question['question'] = questions[i].QUESTION
        question['description'] = questions[i].DESCRIPTION
        question['timestamp'] = questions[i].TIMESTAMP
        question['event_name'] = questions[i].EVENT_KEY.NAME
        answer = get_top_answer(questions[i])
        if answer is None:
            question['answer'] = "null"
        else:
            question['answer'] = answer.ANSWER
            question['upvotes'] = answer.NUM_UPVOTES
            question['answered_by'] = answer.USER_KEY.NAME
            question['answered_at'] = answer.TIMESTAMP
            if is_logged_in:
                question['is_upvoted'] = is_user_upvoted_answer(username, answer.ANSWER_ID)
            else:
                question['is_upvoted'] = false

        question_array.append(question)


    return render(request, 'event_page.html', {'event_name':event.NAME, 'description': event.DESCRIPTION,
                            'registration_open_date':event.REGISTRATION_OPEN_DATE, 'registration_close_date':event.REGISTRATION_CLOSE_DATE,
                            'event_date_1':event.EVENT_DATE_1, 'event_date_2':event.EVENT_DATE_2, 'details':event.DETAILS,
                            'website':event.WEBSITE, 'location':event.LOCATION,
                            'logged_in': is_logged_in, 'is_guide': is_guide, 'is_going': is_going,
                            'guides':guide_array, 'experiences':experience_array, 'questions':question_array})


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
