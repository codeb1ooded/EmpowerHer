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
