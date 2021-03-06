# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-26 14:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Moonshot', '0003_auto_20180226_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='INBOX',
            fields=[
                ('INBOX_ID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('RECEIVER_KEY', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inbox_receiver', to='Moonshot.USER')),
                ('SENDER_KEY', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inbox_sender', to='Moonshot.USER')),
            ],
        ),
    ]
