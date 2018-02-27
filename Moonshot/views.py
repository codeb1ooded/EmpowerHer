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
from Moonshot.models import QUESTION,ANSWER
from fusioncharts import FusionCharts
from django.http import HttpResponse


def user_page(request):
    username = request.GET['username']

    is_logged_in = request.user.is_authenticated
    login_username = None
    if is_logged_in:
        login_username = request.user.username

    user = get_user(username)
    events_guiding = get_user_events_guiding(username)
    events_going = get_user_events_going(username)
    answers = get_user_answers(username)
    questions = get_user_questions(username)
    experiences = get_user_experiences(username)

    question_array = []
    for i in range(0, len(questions)):
        question = {}
        question['question_id'] = questions[i].QUESTION_ID
        question['question'] = questions[i].QUESTION
        question['description'] = questions[i].DESCRIPTION
        question['timestamp'] = questions[i].TIMESTAMP
        question['event_id'] = questions[i].EVENT_KEY.EVENT_ID
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
                question['is_upvoted'] = is_user_upvoted_answer(login_username, answer.ANSWER_ID)
            else:
                question['is_upvoted'] = False
        question_array.append(question)

    experience_array = []
    for i in range(0, len(experiences)):
        experience = {}
        experience['experience_id'] = experiences[i].EXPERIENCE_ID
        experience['experience'] = experiences[i].EXPERIENCE
        experience['event_id'] = experiences[i].EVENT_KEY.EVENT_ID
        experience['event_name'] = experiences[i].EVENT_KEY.NAME
        experience['timestamp'] = experiences[i].TIMESTAMP
        experience['username'] = experiences[i].USER_KEY.USER_REF.username
        experience['name'] = experiences[i].USER_KEY.NAME
        experience['upvotes'] = experiences[i].NUM_UPVOTES
        experience['is_upvoted'] = False
        if is_logged_in:
            experience['is_upvoted'] = is_user_upvoted_experience(login_username, experiences[i].EXPERIENCE_ID)
        else:
            experience['is_upvoted'] = False
        experience_array.append(experience)

    events_guiding_array = []
    for event in events_guiding:
        event_json = {}
        event_json['event_id'] = event.EVENT_KEY.EVENT_ID
        event_json['event_name'] = event.EVENT_KEY.NAME
        event_json['website'] = event.EVENT_KEY.WEBSITE
        event_json['description'] = event.EVENT_KEY.DESCRIPTION
        event_json['is_guide'] = is_user_guide(username, event.EVENT_KEY.EVENT_ID)
        event_json['is_going'] = is_user_going(username, event.EVENT_KEY.EVENT_ID)
        events_guiding_array.append(event_json)

    events_going_array = []
    for event in events_going:
        event_json = {}
        event_json['event_id'] = event.EVENT_KEY.EVENT_ID
        event_json['event_name'] = event.EVENT_KEY.NAME
        event_json['website'] = event.EVENT_KEY.WEBSITE
        event_json['description'] = event.EVENT_KEY.DESCRIPTION
        event_json['is_guide'] = is_user_guide(username, event.EVENT_KEY.EVENT_ID)
        event_json['is_going'] = is_user_going(username, event.EVENT_KEY.EVENT_ID)
        events_going_array.append(event_json)

    context = {'username': username,
                'is_logged_in': is_logged_in,
                'login_username': login_username,
                'user': user,
                'reputation': user.EXPERIENCE_UPVOTE + user.ANSWER_UPVOTE + user.GUIDE_UPVOTE + user.NUM_QUESTION_ASKED,
                'events_guiding': events_guiding_array,
                'events_going': events_going_array,
                'answers': answers,
                'questions': question_array,
                'experiences': experience_array,
                }
    return render(request, 'user.html', context)


def home(request):
    is_logged_in = request.user.is_authenticated
    if is_logged_in:
        return news_feed(request)
    else:
        return render(request, 'home.html')


def sign_in_up_view(request):
    signin_form = UserAuthenticationForm()
    singnup_form = UserRegistrationForm()
    return render(request, 'home.html', {'signin' : signin_form, 'signup':singnup_form})


def sign_in_view(request):
    form = UserAuthenticationForm(request.POST)
    if form.is_valid():
        userObj = form.cleaned_data
        username = userObj['username']
        password =  userObj['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            raise forms.ValidationError('Looks like a username with that email or password is incorrect!!')
    return render(request, template_name, {'form' : form})


def sign_up_view(request):
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
    return render(request, template_name, {'form' : form})


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
    for i in range(0, len(questions)):
        question = {}
        question['question_id'] = questions[i].QUESTION_ID
        question['question'] = questions[i].QUESTION
        question['description'] = questions[i].DESCRIPTION
        question['timestamp'] = questions[i].TIMESTAMP
        question['event_id'] = questions[i].EVENT_KEY.EVENT_ID
        question['event_name'] = questions[i].EVENT_KEY.NAME
        answer = get_top_answer(questions[i])
        if answer is None:
            question['answer'] = "null"
        else:
            question['answer'] = answer.ANSWER
            question['upvotes'] = answer.NUM_UPVOTES
            question['answered_by'] = answer.USER_KEY.NAME
            question['username'] = answer.USER_KEY.USER_REF.username
            question['answered_at'] = answer.TIMESTAMP
            if is_logged_in:
                question['is_upvoted'] = is_user_upvoted_answer(username, answer.ANSWER_ID)
            else:
                question['is_upvoted'] = False

        question_array.append(question)

    exp = get_experience_user_written(username, event_id)
    user_experience = None
    experience_id = -1
    if exp is not None:
        user_experience = exp.EXPERIENCE
        experience_id = exp.EXPERIENCE_ID

    context = {
        'event_id': event.EVENT_ID,
        'event_name':event.NAME,
        'description': event.DESCRIPTION,
        'registration_open_date':event.REGISTRATION_OPEN_DATE,
        'registration_close_date':event.REGISTRATION_CLOSE_DATE,
        'event_date_1':event.EVENT_DATE_1,
        'event_date_2':event.EVENT_DATE_2,
        'details':event.DETAILS,
        'website':event.WEBSITE,
        'location':event.LOCATION,
        'username': username,
        'is_logged_in': is_logged_in,
        'is_guide': is_guide,
        'is_going': is_going,
        'experience':user_experience,
        'experience_id': experience_id,
        'guides':guide_array,
        'experiences':experience_array,
        'questions':question_array
    }
    return render(request, 'event_page.html', context)


def experience_list(request):
    event_id = request.GET['event_id']
    event = get_event_details(event_id)
    experiences = get_all_experiences(event_id)

    is_logged_in = request.user.is_authenticated
    username = None
    if is_logged_in:
        username = request.user.username

    exp = get_experience_user_written(username, event_id)
    user_experience = None
    experience_id = -1
    if exp is not None:
        user_experience = exp.EXPERIENCE
        experience_id = exp.EXPERIENCE_ID

    all_experiences = []
    for i in range(0, len(experiences)):
        experience = {}
        experience['name'] = experiences[i].USER_KEY.NAME
        experience['username'] = experiences[i].USER_KEY.USER_REF.username
        experience['experience'] = experiences[i].EXPERIENCE
        experience['experience_id'] = experiences[i].EXPERIENCE_ID
        experience['timestamp'] = experiences[i].TIMESTAMP
        experience['upvotes'] = experiences[i].NUM_UPVOTES
        experience['is_upvoted'] = False
        if is_logged_in:
            experience['is_upvoted'] = is_user_upvoted_experience(username, experiences[i].EXPERIENCE_ID)
        all_experiences.append(experience)

    context = {
        'event_id': event_id,
        'event_name': event.NAME,
        'all_experiences': all_experiences,
        'is_logged_in': is_logged_in,
        'username':username,
        'experience':user_experience,
        'experience_id': experience_id
    }
    return render(request, "experience.html", context)


def create_event_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    is_logged_in = request.user.is_authenticated
    username = None
    if is_logged_in:
        username = request.user.username
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
            event_id = create_event(username, name, description, reg_start_date, reg_close_date, event_start_date, event_close_date, details, website, location)
        else:
            event_id  = update_event(username, event_id, name, description, reg_start_date, reg_close_date, event_start_date, event_close_date, details, website, location)
        print event_id
        return HttpResponse(event_id)
    else:
        return render(request, 'create_event.html', {'event_id':-1, 'is_logged_in':is_logged_in, 'username':username})


def update_event_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    event_id = request.GET['event_id']
    is_logged_in = request.user.is_authenticated
    username = None
    if is_logged_in:
        username = request.user.username
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
        update_event(username, event_id, name, description, reg_start_date, reg_close_date, event_start_date, event_close_date, details, website, location)
        return render(request, 'create_event.html', {'event_id':event_id, 'name':name, 'description':description, 'is_logged_in': is_logged_in,
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
        update_event(username, event_id, name, description, reg_start_date, reg_close_date, event_start_date, event_close_date, details, website, location)
        return render(request, 'create_event.html', {'event_id':event_id, 'name':name, 'description':description, 'is_logged_in': is_logged_in,
                                                    'reg_start_date':reg_start_date, 'reg_close_date':reg_close_date, 'event_start_date': event_start_date, 'event_close_date': event_close_date,
                                                'details':details, 'website':website, 'location':location})


def answers_for_question(request):
    question_id = request.GET['question_id']
    question = get_question(question_id)
    answers = get_all_answers(question_id)

    is_logged_in = request.user.is_authenticated
    username = None
    if is_logged_in:
        username = request.user.username

    ans = get_user_written_answer(username, question_id)
    user_answer = None
    answer_id = -1
    if ans is not None:
        user_answer = ans.ANSWER
        answer_id = ans.ANSWER_ID
    answers_array = []
    for i in range(0, len(answers)):
        answer = {}
        answer['name'] = answers[i].USER_KEY.NAME
        answer['username'] = answers[i].USER_KEY.USER_REF.username
        answer['answer'] = answers[i].ANSWER
        answer['answer_id'] = answers[i].ANSWER_ID
        answer['timestamp'] = answers[i].TIMESTAMP
        answer['upvotes'] = answers[i].NUM_UPVOTES
        answer['is_upvoted'] = False
        if is_logged_in:
            answer['is_upvoted'] = is_user_upvoted_answer(username, answers[i].ANSWER_ID)
        answers_array.append(answer)
    return render(request, "question.html", {'event_id': question.EVENT_KEY.EVENT_ID, 'event_name': question.EVENT_KEY.NAME, 'is_logged_in': is_logged_in,
                                                    'question':question, 'answers':answers_array, 'username':username, 'answer':user_answer,
                                                    'answer_id': answer_id})


def guide_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    is_logged_in = request.user.is_authenticated
    username = request.user.username
    event_id = request.GET['event_id']
    event = get_event_details(event_id)
    all_guides = get_all_guides(event_id)
    context = {
        'is_logged_in': is_logged_in,
        'username': username,
        'event_id': event.EVENT_ID,
        'event_name': event.NAME,
        'all_guides': all_guides,
    }
    return render(request, "guides.html", context)

def news_feed(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    is_logged_in = request.user.is_authenticated
    username = request.user.username
    user = get_user(username)
    events_going = get_all_events_going(username)
    events = get_all_events()

    all_events = []
    for event in events:
        event_json = {}
        event_json['event_id'] = event.EVENT_ID
        event_json['event_name'] = event.NAME
        event_json['website'] = event.WEBSITE
        event_json['description'] = event.DESCRIPTION
        event_json['is_guide'] = is_user_guide(username, event.EVENT_ID)
        event_json['is_going'] = is_user_going(username, event.EVENT_ID)
        all_events.append(event_json)

    all_experiences = []
    all_questions = []
    all_events_going = []
    for going_event in events_going:
        event_json = {}
        event_json['event_id'] = going_event.EVENT_KEY.EVENT_ID
        event_json['event_name'] = going_event.EVENT_KEY.NAME
        event_json['website'] = going_event.EVENT_KEY.WEBSITE
        event_json['description'] = going_event.EVENT_KEY.DESCRIPTION
        event_json['is_guide'] = is_user_guide(username, going_event.EVENT_KEY.EVENT_ID)
        event_json['is_going'] = is_user_going(username, going_event.EVENT_KEY.EVENT_ID)
        all_events_going.append(event_json)

        experiences = get_all_experiences(going_event.EVENT_KEY.EVENT_ID)
        for i in range(0, len(experiences)):
            experience_json = {}
            experience_json['experience_id'] = experiences[i].EXPERIENCE_ID
            experience_json['experience'] = experiences[i].EXPERIENCE
            experience_json['timestamp'] = experiences[i].TIMESTAMP
            experience_json['username'] = experiences[i].USER_KEY.USER_REF.username
            experience_json['name'] = experiences[i].USER_KEY.NAME
            experience_json['upvotes'] = experiences[i].NUM_UPVOTES
            experience_json['is_upvoted'] = False
            if is_logged_in:
                experience_json['is_upvoted'] = is_user_upvoted_experience(username, experiences[i].EXPERIENCE_ID)
            all_experiences.append(experience_json)

        questions = get_all_questions(going_event.EVENT_KEY.EVENT_ID)
        for i in range(0, len(questions)):
            question_json = {}
            question_json['question_id'] = questions[i].QUESTION_ID
            question_json['question'] = questions[i].QUESTION
            question_json['description'] = questions[i].DESCRIPTION
            question_json['timestamp'] = questions[i].TIMESTAMP
            question_json['event_id'] = questions[i].EVENT_KEY.EVENT_ID
            question_json['event_name'] = questions[i].EVENT_KEY.NAME
            answer = get_top_answer(questions[i])
            if answer is not None:
                question_json['answer'] = answer.ANSWER
                question_json['upvotes'] = answer.NUM_UPVOTES
                question_json['answered_by'] = answer.USER_KEY.NAME
                question_json['answered_at'] = answer.TIMESTAMP
                question_json['is_upvoted'] = False
                if is_logged_in:
                    question_json['is_upvoted'] = is_user_upvoted_answer(username, answer.ANSWER_ID)
            all_questions.append(question_json)

    context = {
            'is_logged_in': is_logged_in,
            'username': username,
            'name': user.NAME,
            'all_events_going': all_events_going,
            'all_events' : all_events,
            'all_experiences': all_experiences,
            'all_questions': all_questions,
        }
    return render(request, "newsfeed.html", context)


def dashboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    # setting chart cosmetics
    dataSource['chart'] = {
      "caption" : "User Performance",
        "numberPrefix": "",
        "theme": "zune"
      }

    is_logged_in = request.user.is_authenticated
    if request.user.is_authenticated():
        user = request.user

    dataSource['categories'] = []
    dataSource['dataset'] = []
    data = {}
    data['category'] = []

    # The data for the chart should be in an array wherein each element of the array is a JSON object as
      # `label` and `value` keys.
      # Iterate through the data in `Country` model and insert in to the `dataSource['data']` list.
    for key in USER.objects.all():
        some = {}
        some['label'] = key.NAME
        data['category'].append(some)
        dataSource['categories'].append(data)

    data = {}
    data['data'] = []
    data['seriesname'] = "Questions Asked"
    for key in USER.objects.all():
        some = {}
        some['value'] = key.NUM_QUESTION_ASKED
        data['data'].append(some)
    dataSource['dataset'].append(data)

    data = {}
    data['data'] = []
    data['seriesname'] = "Total Guide Votes"
    for key in USER.objects.all():
        some = {}
        some['value'] = key.GUIDE_UPVOTE
        data['data'].append(some)
    dataSource['dataset'].append(data)

    data = {}
    data['data'] = []
    data['seriesname'] = "Total Answer Votes"
    for key in USER.objects.all():
        some = {}
        some['value'] = key.ANSWER_UPVOTE
        data['data'].append(some)
    dataSource['dataset'].append(data)

    data = {}
    data['data'] = []
    data['seriesname'] = "Total Experience Votes"
    for key in USER.objects.all():
        some = {}
        some['value'] = key.EXPERIENCE_UPVOTE
        data['data'].append(some)
    dataSource['dataset'].append(data)

    b = USER.objects.get(USER_REF = user)
    b1 = b.BADGE1
    b2 = b.BADGE2
    b3 = b.BADGE3
    b4 = b.BADGE4
    b5 = b.BADGE5

    created_events = get_created_events(user.username)
      # Create an object for the Column 2D chart using the FusionCharts class constructor
    column2D = FusionCharts("mscolumn2d", "ex1" , "600", "400", "chart-1", "json", dataSource)
      # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    return render(request, 'dashboard.html', {'output': column2D.render(),'B':b,'B1':b1,'B2':b2,'B3':b3,'B4':b4,'B5':b5,
                                                'inbox':get_all_inbox(user.username), 'user': b, 'created_events': created_events,
                                                'username':user.username, 'is_logged_in': is_logged_in})
