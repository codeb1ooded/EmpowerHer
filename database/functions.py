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


def get_all_guides(event_id):
    guides = GUIDE_AVAILABLE.objects.filter(EVENT_KEY = event_id)
    return guides


def get_all_experiences(event_id):
    experiences = EXPERIENCE.objects.filter(EVENT_KEY = event_id)
    return experiences


def get_all_questions(event_id):
    questions = QUESTION.objects.filter(EVENT_KEY = event_id)
    return questions


def get_question(question_id):
    question = QUESTION.objects.filter(QUESTION_ID = question_id)[0]
    return question


def get_all_answers(question_id):
    question = get_question(question_id)
    answers = ANSWER.objects.filter(QUESTION_KEY = question)
    return answers


def get_answer(answer_id):
    answer = ANSWER.objects.filter(ANSWER_ID = answer_id)
    try:
        return answer[0]
    except:
        return None


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


def up_down_vote_experience(username, experience_id, upvote):
    user = get_user(username)
    experience = get_experience(experience_id)
    upvoteid = username + "-" + experience_id
    if upvote:
        query_upvote = UPVOTE_EXPERIENCE( UPVOTE_EXPERIENCE_ID = upvoteid,
                                            USER_KEY = user,
                                            EXPERIENCE_KEY = experience) # foreign key need to be done
        query_upvote.save()
        EXPERIENCE.objects.filter(EXPERIENCE_ID = experience_id).update (NUM_UPVOTES = experience.NUM_UPVOTES + 1)
        return experience.NUM_UPVOTES + 1
    else:
        UPVOTE_EXPERIENCE.objects.filter(UPVOTE_EXPERIENCE_ID = upvoteid).delete()
        EXPERIENCE.objects.filter(EXPERIENCE_ID = experience_id).update (NUM_UPVOTES = experience.NUM_UPVOTES - 1)
        return experience.NUM_UPVOTES - 1


def up_down_vote_answer(username, answer_id, upvote):
    user = get_user(username)
    answer = get_answer(answer_id)
    upvoteid = username + "-" + answer_id
    if upvote:
        query_upvote = UPVOTE_ANSWER( UPVOTE_ANSWER_ID = upvoteid,
                                            USER_KEY = user,
                                            ANSWER_KEY = answer)
        query_upvote.save()
        ANSWER.objects.filter(ANSWER_ID = answer_id).update (NUM_UPVOTES = answer.NUM_UPVOTES + 1)
        return answer.NUM_UPVOTES + 1
    else:
        UPVOTE_ANSWER.objects.filter(UPVOTE_ANSWER_ID = upvoteid).delete()
        ANSWER.objects.filter(ANSWER_ID = answer_id).update (NUM_UPVOTES = answer.NUM_UPVOTES - 1)
        return answer.NUM_UPVOTES - 1


def user_going(username, event_id, going):
    user = get_user(username)
    event = get_event_details(event_id)
    going_id = username + "-" + event_id
    if going:
        query_going = GOING_EVENT(GOING_ID = going_id, USER_KEY = user, EVENT_KEY = event)
        query_going.save()
    else :
        GOING_EVENT.objects.filter(GOING_ID = going_id).delete()
    return not going


def user_guiding(username, event_id, guiding):
    user = get_user(username)
    event = get_event_details(event_id)
    guiding_id = username + "-" + event_id
    if guiding:
        query_guiding = GUIDE_AVAILABLE(GUIDE_ID = guiding_id, USER_KEY = user, EVENT_KEY = event)
        query_guiding.save()
    else :
        GUIDE_AVAILABLE.objects.filter(GUIDE_ID = guiding_id).delete()
    return not guiding
