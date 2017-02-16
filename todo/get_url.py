#coding: utf-8
from django.conf import settings
import requests


def GetOrgStructure(user):
    """
    获取用户组织架构
    :return:
    """
    url = 'http://service.example.com/restful/subuser/get/'
    username = settings.TOKEN_USER
    password = settings.TOKEN_PASSWORD
    data = {
        'username': username,
        'password': password,
        'user': user,
    }
    try:
        res = requests.get(url, params=data, timeout=3)

        if res.status_code == 200:
            result = res.json()
            if result.get('code') == 0:
                return result.get('msg')
            else:
                return False
        else:
            return False

    except:
        return False


