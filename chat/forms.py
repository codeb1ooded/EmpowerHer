from django import forms
from Moonshot.models import LIVE_CHAT

class PostForm:

    class Meta:
        model = LIVE_CHAT
        fields = ('sender_name','message',)
        

