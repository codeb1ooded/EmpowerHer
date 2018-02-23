from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import *
from django.contrib.auth.models import User
from django.http import *
from django.conf import settings
import json

from .models import EXPERIENCE
from django.template import loader

from database.functions import *
from Moonshot.forms import *

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
        experience['experience_id'] = experiences[i].EXPERIENCE_ID
        experience['experience'] = experiences[i].EXPERIENCE
        experience['timestamp'] = experiences[i].TIMESTAMP
        experience['username'] = experiences[i].USER_KEY.USER_REF.username
        experience['name'] = experiences[i].USER_KEY.NAME
        experience['upvotes'] = experiences[i].NUM_UPVOTES
        experience['is_upvoted'] = False
        if is_logged_in:
            experience['is_upvoted'] = is_user_upvoted_experience(username, experiences[i].EXPERIENCE_ID)
        else:
            experience['is_upvoted'] = False
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
                question['is_upvoted'] = False

        question_array.append(question)


    EVENT_ID = models.IntegerField(primary_key=True)
    return render(request, 'event_page.html', {'event_name':event.NAME, 'description': event.DESCRIPTION, 'event_id': event.EVENT_ID,
                            'registration_open_date':event.REGISTRATION_OPEN_DATE, 'registration_close_date':event.REGISTRATION_CLOSE_DATE,
                            'event_date_1':event.EVENT_DATE_1, 'event_date_2':event.EVENT_DATE_2, 'details':event.DETAILS,
                            'website':event.WEBSITE, 'location':event.LOCATION,
                            'username': username,
                            'logged_in': is_logged_in, 'is_guide': is_guide, 'is_going': is_going,
                            'guides':guide_array, 'experiences':experience_array, 'questions':question_array})


def experience_list(request):
    event_id = request.GET['event_id']
    all_experiences = get_all_experiences(event_id)
    template = loader.get_template('experience.html')
    context = {
        'all_experiences': all_experiences,
    }
    return render(request, "experience.html", context)


#@login_required
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


def create_event_view(request):
    if 'event_id' in request.GET:
        event_id = request.GET['event_id']
        name = request.GET['name']
        description = request.GET['description']
        reg_start_date = request.GET['reg_start_date']
        reg_close_date = request.GET['reg_close_date']
        event_start_date = request.GET['event_start_date']
        event_close_date = request.GET['event_close_date']
        details = request.GET['details']
        website = request.GET['website']
        location = request.GET['location']
        if event_id == '-1':
            event_id = create_event(name, description, reg_start_date, reg_close_date, event_start_date, event_close_date, details, website, location)
        else:
            event_id  = update_event(event_id, name, description, reg_start_date, reg_close_date, event_start_date, event_close_date, details, website, location)
        print event_id
        return HttpResponse(event_id)
    else:
        return render(request, 'create_event.html', {'event_id':-1})


def update_event_view(request):
    event_id = request.GET['event_id']
    print "Upadte"
    if 'name' in request.GET:
        name = request.GET['name']
        description = request.GET['description']
        reg_start_date = request.GET['reg_start_date']
        reg_close_date = request.GET['reg_close_date']
        event_start_date = request.GET['event_start_date']
        event_close_date = request.GET['event_close_date']
        details = request.GET['details']
        website = request.GET['website']
        location = request.GET['location']
        update_event(event_id, name, description, reg_start_date, reg_close_date, event_start_date, event_close_date, details, website, location)
        return render(request, 'create_event.html', {'event_id':event_id, 'name':name, 'description':description,
                                                    'reg_start_date':reg_start_date, 'reg_close_date':reg_close_date, 'event_start_date': event_start_date, 'event_close_date': event_close_date,
                                                'details':details, 'website':website, 'location':location})
    else:
        event = get_event_details(event_id)
        name = event.NAME
        description = event.DESCRIPTION
        reg_start_date = event.REGISTRATION_OPEN_DATE
        reg_close_date = event.REGISTRATION_CLOSE_DATE
        event_start_date = event.EVENT_DATE_1
        event_close_date = event.EVENT_DATE_2
        details = event.DETAILS
        website = event.WEBSITE
        location = event.LOCATION
        update_event(event_id, name, description, reg_start_date, reg_close_date, event_start_date, event_close_date, details, website, location)
        return render(request, 'create_event.html', {'event_id':event_id, 'name':name, 'description':description,
                                                    'reg_start_date':reg_start_date, 'reg_close_date':reg_close_date, 'event_start_date': event_start_date, 'event_close_date': event_close_date,
                                                'details':details, 'website':website, 'location':location})


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
