# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-17 23:30
from __future__ import unicode_literals

from django.db import migrations, models
from osf.models.oauth import ApiOAuth2PersonalToken, ApiOAuth2Scope


def remove_m2m_scopes(state, schema):
    tokens = ApiOAuth2PersonalToken.objects.all()
    for token in tokens:
        token.scope_temp.clear()
        token.save()

def migrate_scopes_from_char_to_m2m(state, schema):
    tokens = ApiOAuth2PersonalToken.objects.all()
    # Loop inside loop? How many tokens do we have on prod?
    for token in tokens:
        string_scopes = token.scopes.split(' ')
        for scope in string_scopes:
            token.scopes_temp.add(ApiOAuth2Scope.objects.get(name=scope))
            token.save()

class Migration(migrations.Migration):

    dependencies = [
        ('osf', '0138_merge_20181012_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='apioauth2personaltoken',
            name='scopes_temp',
            field=models.ManyToManyField(related_name='tokens', to='osf.ApiOAuth2Scope'),
        ),
        migrations.RunPython(
            migrate_scopes_from_char_to_m2m,
            remove_m2m_scopes
        )
    ]
