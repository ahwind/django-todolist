#coding: utf-8
import requests
import json


class Notification(object):

    def __init__(self, title):
        self.email_url = 'http://msg.example.com/notify'
        self.email_payload = {
            'sender': '任务管理系统',
            'sub': '%s' % title,
            'msg': '',
            'user': '',
            'method': 'mail'
        }

    def send_email(self, user, msg):
        self.email_payload['user'] = user
        self.email_payload['msg'] = msg
        data = json.dumps(self.email_payload)
        try:
            response = requests.post(self.email_url, data, timeout=3)
        except:
            return False

        return True


    def send_wecat(self):
        pass




