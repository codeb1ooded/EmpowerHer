from django.contrib.auth.models import User
from django.db.models import Q

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

def create_event(username, name, description, reg_start_date, reg_close_date, event_start_date, event_close_date, details, website, location):
    event_id = len(EVENT.objects.all()) + 1
    user = get_user(username)
    query_add_event = EVENT( EVENT_ID = event_id,
							   NAME = name,
							   DESCRIPTION = description,
							   REGISTRATION_OPEN_DATE = reg_start_date,
							   REGISTRATION_CLOSE_DATE = reg_close_date,
					   		   EVENT_DATE_1 = event_start_date,
					   		   EVENT_DATE_2 = event_close_date,
					   		   DETAILS = details,
					   		   WEBSITE = website,
					   		   LOCATION = location,
                               USER_KEY = user)
    query_add_event.save()
    query_check_event_added = EVENT.objects.filter(EVENT_ID = event_id)[0]
    try:
        return query_check_event_added.EVENT_ID
    except:
        return -1


def update_event(username, event_id, name, description, reg_start_date, reg_close_date, event_start_date, event_close_date, details, website, location):
    user = get_user(username)
    query_add_event = EVENT( EVENT_ID = event_id,
							   NAME = name,
							   DESCRIPTION = description,
							   REGISTRATION_OPEN_DATE = reg_start_date,
							   REGISTRATION_CLOSE_DATE = reg_close_date,
					   		   EVENT_DATE_1 = event_start_date,
					   		   EVENT_DATE_2 = event_close_date,
					   		   DETAILS = details,
					   		   WEBSITE = website,
					   		   LOCATION = location,
                               USER_KEY = user)
    query_add_event.save()
    query_check_event_added = EVENT.objects.filter(EVENT_ID = event_id)[0]
    try:
        return query_check_event_added.EVENT_ID
    except:
        return -1


def submit_answer(question_id, answer, username):
    ans_id = len(ANSWER.objects.all()) + 1
    question = get_question(question_id)
    user = get_user(username)
    event = question.EVENT_KEY
    query_add_answer = ANSWER( ANSWER_ID = ans_id,
							   ANSWER = answer,
							   TIMESTAMP = datetime.datetime.now(),
							   NUM_UPVOTES = 0,
							   EVENT_KEY = event,
					   		   USER_KEY = user,
					   		   QUESTION_KEY = question)
    query_add_answer.save()
    query_check_answer_added = ANSWER.objects.filter(ANSWER_ID = ans_id)[0]
    try:
        return query_check_answer_added.ANSWER_ID
    except:
        return -1


def update_answer(question_id, answer_id, answer, username):
    question = get_question(question_id)
    user = get_user(username)
    event = question.EVENT_KEY
    query_add_answer = ANSWER( ANSWER_ID = answer_id,
							   ANSWER = answer,
							   TIMESTAMP = datetime.datetime.now(),
							   NUM_UPVOTES = 0,
							   EVENT_KEY = event,
					   		   USER_KEY = user,
					   		   QUESTION_KEY = question)
    query_add_answer.save()
    query_check_answer_added = ANSWER.objects.filter(ANSWER_ID = answer_id)[0]
    try:
        return query_check_answer_added.ANSWER_ID
    except:
        return -1


def submit_experience(event_id, experience, username):
    exp_id = len(EXPERIENCE.objects.all()) + 1
    event = get_event_details(event_id)
    user = get_user(username)
    query_add_experience = EXPERIENCE( EXPERIENCE_ID = exp_id,
							   EXPERIENCE = experience,
							   TIMESTAMP = datetime.datetime.now(),
							   NUM_UPVOTES = 0,
							   EVENT_KEY = event,
					   		   USER_KEY = user)
    query_add_experience.save()
    query_check_experience_added = EXPERIENCE.objects.filter(EXPERIENCE_ID = exp_id)[0]
    try:
        return query_check_experience_added.EXPERIENCE_ID
    except:
        return -1


def update_experience(experience_id, event_id, experience, username):
    event = get_event_details(event_id)
    user = get_user(username)
    query_add_experience = EXPERIENCE( EXPERIENCE_ID = experience_id,
							   EXPERIENCE = experience,
							   TIMESTAMP = datetime.datetime.now(),
							   NUM_UPVOTES = 0,
							   EVENT_KEY = event,
					   		   USER_KEY = user)
    query_add_experience.save()
    query_check_experience_added = EXPERIENCE.objects.filter(EXPERIENCE_ID = experience_id)[0]
    try:
        return query_check_experience_added.EXPERIENCE_ID
    except:
        return -1


def submit_question(event_id, question, username):
    ques_id = len(QUESTION.objects.all()) + 1
    event = get_event_details(event_id)
    user = get_user(username)
    query_add_question = QUESTION( QUESTION_ID = ques_id,
							   QUESTION = question,
                               DESCRIPTION = 'NA',
							   TIMESTAMP = datetime.datetime.now(),
							   EVENT_KEY = event,
					   		   USER_KEY = user)
    query_add_question.save()
    query_check_question_added = QUESTION.objects.filter(QUESTION_ID = ques_id)[0]
    try:
        return query_check_question_added.QUESTION_ID
    except:
        return -1

def store_message(sender_username, receiver_username, message):
    message_id = len(LIVE_CHAT.objects.all()) + 1
    sender = get_user(sender_username)
    receiver = get_user(receiver_username)
    messageObj = LIVE_CHAT( CHAT_ID=message_id,
                            TIMESTAMP = datetime.datetime.now(),
                            MESSAGE = message,
                            SENDER_KEY = sender,
                            RECEIVER_ID = receiver)
    messageObj.save()

    inbox_id_1 = sender_username + "-" +  receiver_username
    inbox1 = INBOX(INBOX_ID=inbox_id_1, SENDER_KEY=sender, RECEIVER_KEY=receiver)
    inbox1.save()

    inbox_id_2 = receiver_username + "-" +  sender_username
    inbox2 = INBOX(INBOX_ID=inbox_id_2, SENDER_KEY=receiver, RECEIVER_KEY=sender)
    inbox2.save()

    message_check = LIVE_CHAT.objects.filter(SENDER_KEY = sender, RECEIVER_ID = receiver)[0]
    try:
        return message_check.CHAT_ID
    except:
        return -1


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


def get_all_messages(sender_username, receiver_username):
    sender = get_user(sender_username)
    receiver = get_user(receiver_username)
    messages = LIVE_CHAT.objects.filter(
                        (Q(SENDER_KEY=sender) & Q(RECEIVER_ID=receiver)) |
                        (Q(SENDER_KEY=receiver) & Q(RECEIVER_ID=sender))).order_by('TIMESTAMP')
    print messages
    return messages


def get_all_inbox(username):
    user = get_user(username)
    inbox = INBOX.objects.filter(SENDER_KEY=user)
    return inbox


def get_user_written_answer(username, question_id):
    user = get_user(username)
    question = get_question(question_id)
    answer = ANSWER.objects.filter(USER_KEY = user, QUESTION_KEY=question)
    try:
        return answer[0]
    except:
        return None


def get_experience_user_written(username, event_id):
    user = get_user(username)
    event = get_event_details(event_id)
    experience = EXPERIENCE.objects.filter(USER_KEY = user, EVENT_KEY=event)
    try:
        return experience[0]
    except:
        return None


def get_top_answer(question_obj):
    answers = ANSWER.objects.filter(QUESTION_KEY=question_obj).order_by('-NUM_UPVOTES')
    try:
        return answers[0]
    except:
        return None


def get_user_events_guiding(username):
    user = get_user(username)
    return GUIDE_AVAILABLE.objects.filter(USER_KEY=user)


def get_user_events_going(username):
    user = get_user(username)
    return GOING_EVENT.objects.filter(USER_KEY=user)


def get_user_answers(username):
    user = get_user(username)
    return ANSWER.objects.filter(USER_KEY=user)


def get_user_questions(username):
    user = get_user(username)
    return QUESTION.objects.filter(USER_KEY=user)


def get_user_experiences(username):
    user = get_user(username)
    return EXPERIENCE.objects.filter(USER_KEY=user)


def get_created_events(username):
    user = get_user(username)
    return EVENT.objects.filter(USER_KEY=user)


def get_number_of_questions(username):
    user = get_user(username)
    questions = QUESTION.objects.filter(USER_KEY=user)
    return len(questions)


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


def is_user_upvoted_experience(username, experience_id):
    user = get_user(username)
    experience = get_experience(experience_id)
    return len(UPVOTE_EXPERIENCE.objects.filter(USER_KEY=user, EXPERIENCE_KEY=experience)) > 0


def up_down_vote_experience(username, experience_id, upvote):
    user = get_user(username)
    experience = get_experience(experience_id)
    upvoteid = username + "-" + experience_id
    inbuilt_user = experience.USER_KEY.USER_REF
    user_upvotes = get_user(experience.USER_KEY.USER_REF.username).EXPERIENCE_UPVOTE
    if upvote:
        query_upvote = UPVOTE_EXPERIENCE( UPVOTE_EXPERIENCE_ID = upvoteid,
                                            USER_KEY = user,
                                            EXPERIENCE_KEY = experience)
        query_upvote.save()
        USER.objects.filter(USER_REF=inbuilt_user).update(EXPERIENCE_UPVOTE = user_upvotes+1)
        EXPERIENCE.objects.filter(EXPERIENCE_ID = experience_id).update (NUM_UPVOTES = experience.NUM_UPVOTES + 1)
        return experience.NUM_UPVOTES + 1
    else:
        UPVOTE_EXPERIENCE.objects.filter(UPVOTE_EXPERIENCE_ID = upvoteid).delete()
        USER.objects.filter(USER_REF=inbuilt_user).update(EXPERIENCE_UPVOTE = user_upvotes-1)
        EXPERIENCE.objects.filter(EXPERIENCE_ID = experience_id).update (NUM_UPVOTES = experience.NUM_UPVOTES - 1)
        return experience.NUM_UPVOTES - 1


def up_down_vote_answer(username, answer_id, upvote):
    user = get_user(username)
    answer = get_answer(answer_id)
    upvoteid = username + "-" + answer_id
    inbuilt_user = answer.USER_KEY.USER_REF
    user_upvotes = get_user(answer.USER_KEY.USER_REF.username).ANSWER_UPVOTE
    if upvote:
        query_upvote = UPVOTE_ANSWER( UPVOTE_ANSWER_ID = upvoteid,
                                            USER_KEY = user,
                                            ANSWER_KEY = answer)
        query_upvote.save()
        USER.objects.filter(USER_REF=inbuilt_user).update(ANSWER_UPVOTE = user_upvotes+1)
        ANSWER.objects.filter(ANSWER_ID = answer_id).update (NUM_UPVOTES = answer.NUM_UPVOTES + 1)
        return answer.NUM_UPVOTES + 1
    else:
        UPVOTE_ANSWER.objects.filter(UPVOTE_ANSWER_ID = upvoteid).delete()
        USER.objects.filter(USER_REF=inbuilt_user).update(ANSWER_UPVOTE = user_upvotes-1)
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


def get_all_events_going(username):
    user=get_user(username)
    all_events_going = GOING_EVENT.objects.filter(USER_KEY = user)
    return all_events_going

def get_all_events():
    all_events = EVENT.objects.all()
    return all_events
