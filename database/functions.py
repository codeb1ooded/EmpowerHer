from django.contrib.auth.models import User

from datetime import date

from Moonshot.models import *

def create_user(user, name):
    query_add_user = USER( USER_REF = user,
							   NAME = name,
							   PROFILE_LINK = user.username,
							   EXPERIENCE_UPVOTE = 0,
							   ANSWER_UPVOTE = 0,
					   		   GUIDE_UPVOTE = 0,
					   		   NUM_QUESTION_ASKED = 0,
					   		   BADGE1 = False,
					   		   BADGE2 = False,
					   		   BADGE3 = False,
					   		   BADGE4 = False,
					   		   BADGE5 = False ) # foreign key need to be done
    query_add_user.save()
    query_check_user_added = USER.objects.filter(USER_REF = user)
    try:
    	print(query_check_user_added[0].username)
        return True
    except:
        return False


def get_user(username):
    inbuilt_user = User.objects.filter(username=username)
    user = USER.objects.filter(USER_REF = inbuilt_user)
    try:
        return user[0]
    except:
        return None


def get_event_details(event_id):
    event = EVENT.objects.filter(EVENT_ID = event_id)
    try:
    	print(event[0].NAME)
        return event[0]
    except:
        return None


def get_experience(experience_id):
    experience = EXPERIENCE.objects.filter(EXPERIENCE_ID = experience_id)
    try:
        return experience[0]
    except:
        return None


def get_answer(answer_id):
    answer = ANSWER.objects.filter(ANSWER_ID = answer_id)
    try:
        return answer[0]
    except:
        return None


def get_all_guides(event_id):
    guides = GUIDE_AVAILABLE.objects.filter(EVENT_KEY = event_id)
    return guides


def get_all_experiences(event_id):
    experiences = EXPERIENCE.objects.filter(EVENT_KEY = event_id)
    return experiences


def get_all_questions(event_id):
    questions = QUESTION.objects.filter(EVENT_KEY = event_id)
    return questions


def get_top_answer(question_obj):
    answers = ANSWER.objects.filter(QUESTION_KEY=question_obj).order_by('-NUM_UPVOTES')
    try:
        return answers[0]
    except:
        return None


def is_user_guide(username, event_id):
    user = get_user(username)
    event = get_event_details(event_id)
    return len(GUIDE_AVAILABLE.objects.filter(USER_KEY=user, EVENT_KEY=event)) > 0


def is_user_going(username, event_id):
    user = get_user(username)
    event = get_event_details(event_id)
    return len(GOING_EVENT.objects.filter(USER_KEY=user, EVENT_KEY=event)) > 0


def is_user_upvoted_experience(username, experience_id):
    user = get_user(username)
    experience = get_experience(experience_id)
    return len(UPVOTE_EXPERIENCE.objects.filter(USER_KEY=user, EXPERIENCE_KEY=experience)) > 0


def is_user_upvoted_answer(username, answer_id):
    user = get_user(username)
    answer = get_answer(answer_id)
    return len(UPVOTE_ANSWER.objects.filter(USER_KEY=user, ANSWER_KEY=answer)) > 0
