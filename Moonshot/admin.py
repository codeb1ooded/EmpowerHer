from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(USER)
admin.site.register(EVENT)
admin.site.register(QUESTION)
admin.site.register(ANSWER)
admin.site.register(EXPERIENCE)
admin.site.register(GUIDE_AVAILABLE)
admin.site.register(TAG)
admin.site.register(TAGGED_EVENT)
admin.site.register(GOING_EVENT)
admin.site.register(UPVOTE_ANSWER)
admin.site.register(UPVOTE_EXPERIENCE)
admin.site.register(UPVOTE_GUIDE)
admin.site.register(LIVE_CHAT)
