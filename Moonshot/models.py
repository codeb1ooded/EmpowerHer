from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import *

import datetime


class USER(models.Model):
    USER_REF = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="USER")
    NAME = models.CharField(max_length=100)
    PROFILE_LINK = models.CharField(max_length=100)
    EXPERIENCE_UPVOTE = models.IntegerField()
    ANSWER_UPVOTE = models.IntegerField()
    GUIDE_UPVOTE = models.IntegerField()
    NUM_QUESTION_ASKED = models.IntegerField()
    BADGE1 = models.BooleanField(default=False)
    BADGE2 = models.BooleanField(default=False)
    BADGE3 = models.BooleanField(default=False)
    BADGE4 = models.BooleanField(default=False)
    BADGE5 = models.BooleanField(default=False)

    def __str__(self):
		return self.NAME + '\tKarma Score: ' + str(self.EXPERIENCE_UPVOTE + self.ANSWER_UPVOTE + self.GUIDE_UPVOTE)


class EVENT(models.Model):
    EVENT_ID = models.IntegerField(primary_key=True)
    NAME = models.CharField(max_length=100)
    DESCRIPTION = models.CharField(max_length=1000)
    REGISTRATION_OPEN_DATE = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    REGISTRATION_CLOSE_DATE = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    EVENT_DATE_1 = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    EVENT_DATE_2 = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    DETAILS = models.CharField(max_length=50000)
    WEBSITE = models.CharField(max_length=200)
    LOCATION = models.CharField(max_length=200)
    USER_KEY = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
		null=True,
		blank=True,
    )

    def __str__(self):
		return self.NAME + '\n' + self.WEBSITE


class QUESTION(models.Model):
    QUESTION_ID = models.IntegerField(primary_key=True)
    QUESTION = models.CharField(max_length=1000)
    DESCRIPTION = models.CharField(max_length=1000)
    TIMESTAMP = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    EVENT_KEY = models.ForeignKey(
        EVENT,
		null=True,
		blank=True,
    )
    USER_KEY = models.ForeignKey(
        USER,
		null=True,
		blank=True,
    )

    def __str__(self):
		return self.QUESTION + '\n' + self.EVENT_KEY.NAME


class ANSWER(models.Model):
    ANSWER_ID = models.IntegerField(primary_key=True)
    ANSWER = models.CharField(max_length=100000)
    TIMESTAMP = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    NUM_UPVOTES = models.IntegerField(default=0)
    EVENT_KEY = models.ForeignKey(
        EVENT,
		null=True,
		blank=True,
    )
    USER_KEY = models.ForeignKey(
        USER,
		null=True,
		blank=True,
    )
    QUESTION_KEY = models.ForeignKey(
        QUESTION ,
		null=True,
		blank=True,
    )

    def __str__(self):
		return self.ANSWER + '\n' + self.EVENT_KEY.NAME


class EXPERIENCE(models.Model):
    EXPERIENCE_ID = models.IntegerField(primary_key=True)
    EXPERIENCE = models.CharField(max_length=100000)
    TIMESTAMP = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    NUM_UPVOTES = models.IntegerField(default=0)
    EVENT_KEY = models.ForeignKey(
        EVENT,
		null=True,
		blank=True,
    )
    USER_KEY = models.ForeignKey(
        USER,
		null=True,
		blank=True,
    )

    def __str__(self):
		return self.EVENT_KEY.NAME + " By " + self.USER_KEY.NAME


class GUIDE_AVAILABLE(models.Model):
    GUIDE_ID = models.CharField(primary_key=True, max_length=100) # (username + "-" = event_id)
    ''' Score related to guidance '''
    EVENT_KEY = models.ForeignKey(
        EVENT,
		null=True,
		blank=True,
    )
    USER_KEY = models.ForeignKey(
        USER,
		null=True,
		blank=True,
    )

    def __str__(self):
		return self.EVENT_KEY.NAME + " By " + self.USER_KEY.NAME


class TAG(models.Model):
    TAG_ID = models.IntegerField(primary_key=True)
    NAME = models.CharField(max_length=1000)

    def __str__(self):
		return self.NAME


class TAGGED_EVENT(models.Model):
    RELATION_ID = models.IntegerField(primary_key=True)
    TAG_KEY = models.ForeignKey(
        TAG,
		null=True,
		blank=True,
    )
    EVENT_KEY = models.ForeignKey(
        EVENT,
		null=True,
		blank=True,
    )

    def __str__(self):
		return self.TAG_KEY.NAME + self.EVENT_KEY.NAME


class GOING_EVENT(models.Model):
    GOING_ID = models.CharField(primary_key=True, max_length=100) # (username + "-" = event_id)
    EVENT_KEY = models.ForeignKey(
        EVENT,
		null=True,
		blank=True,
    )
    USER_KEY = models.ForeignKey(
        USER,
		null=True,
		blank=True,
    )

    def __str__(self):
		return self.EVENT_KEY.NAME


class UPVOTE_ANSWER(models.Model):
    UPVOTE_ANSWER_ID = models.CharField(primary_key=True, max_length=100) # (username + "-" + answer_id)
    ANSWER_KEY = models.ForeignKey(
        ANSWER,
		null=True,
		blank=True,
    )
    USER_KEY = models.ForeignKey(
        USER,
		null=True,
		blank=True,
    )

    def __str__(self):
		return self.ANSWER_KEY.EVENT_KEY.NAME


class UPVOTE_EXPERIENCE(models.Model):
    UPVOTE_EXPERIENCE_ID = models.CharField(primary_key=True, max_length=100) # (username + "-" + experience_id)
    EXPERIENCE_KEY = models.ForeignKey(
        EXPERIENCE,
		null=True,
		blank=True,
    )
    USER_KEY = models.ForeignKey(
        USER,
		null=True,
		blank=True,
    )

    def __str__(self):
		return self.EXPERIENCE_KEY.EVENT_KEY.NAME


class UPVOTE_GUIDE(models.Model):
    UPVOTE_GUIDE_ID = models.IntegerField(primary_key=True)
    GUIDE_KEY = models.ForeignKey(
        USER,
		null=True,
		blank=True,
        related_name='guide',
    )
    USER_KEY = models.ForeignKey(
        USER,
		null=True,
		blank=True,
        related_name='guided',
    )

    def __str__(self):
		return self.GUIDE_KEY.NAME


class LIVE_CHAT(models.Model):
    CHAT_ID = models.IntegerField(primary_key=True)
    TIMESTAMP = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    MESSAGE = models.CharField(max_length=1000)
    SENDER_KEY = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='sender'
    )
    RECEIVER_ID = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name='receiver'
    )

    def __str__(self):
        return self.MESSAGE


class INBOX(models.Model):
    INBOX_ID = models.CharField(primary_key=True, max_length=100) # (sender_username + "-" + receiver_username)
    SENDER_KEY = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='inbox_sender'
    )
    RECEIVER_KEY = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name='inbox_receiver'
    )
