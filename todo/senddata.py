#coding: utf-8
from django.conf import settings
import requests
import json


def SendTodoData(**kwargs):

    url = settings.PERFURL
    username = settings.TOKEN_USER
    password = settings.TOKEN_PASSWORD

    title = kwargs.get('title')

    value = kwargs.get('value')

    owner = kwargs.get('owner')
 
    type = kwargs.get('type')

    Data = {
        'username': username,
        'password': password,
        'title': title,
        'source': 'todo',
        'value': str(value),
        'owner': owner,
        'type': type,
    }

    response = requests.post(url, data=json.dumps(Data))
    result = response.json()
    if result.get('code') == 0:
        return True
    else:
        return False
