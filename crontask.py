#!/usr/local/python/bin/python
#coding:utf-8
#
import os
import datetime
import requests
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todolist.settings")
django.setup()
from todo.models import CronTask, Item
from django.contrib.auth.models import User
from todo.sendmail import Notification

ActiveCronTask = CronTask.objects.filter(is_active=True)


def Is_First_Day(period):
    """
    period支持weekday/month

    """
    today = datetime.datetime.today()
    weekday = today.isoweekday()

    curr_day = today.day
    curr_month = today.month
    if period == 'weekday':
        if weekday == 1:
            return True

    elif period == 'month':
        if curr_day == 1:
            return True
    elif period == 'quarter':
        if curr_day == 1 and curr_month in [1, 4, 7, 10]:
            return True
    return False

def Is_Holiday(currentdate):

    url = 'http://www.easybots.cn/api/holiday.php?d=%s' % currentdate

    try:
        res = requests.get(url)
        if res.status_code == 200:
            result = res.json()
            for v in result.values():
                if v == '0':
                    return False

    except:
        a = Notification(u'任务管理系统报警信息')

        msg = u'节假日接口获取失败'

        a.send_email('zhangsan', msg)

        return False
    return True

if __name__ == '__main__':

    today = datetime.datetime.today()
    currentdate = today.strftime("%Y%m%d")
    weekdate = [(today + datetime.timedelta(i)).strftime("%Y%m%d") for i in range(0, 6)]
    currentweek = ','.join(weekdate)

    todayisholiday = Is_Holiday(currentdate)

    for t in ActiveCronTask:

        period = t.period

        #对于每天执行任务， 非节假日每天创建任务

        if period == 'day':

            if todayisholiday:
                continue

            for u in t.assigned_to.all():
                try:
                    GetUser = User.objects.get(username=u.username)

                    crontask = Item(title=t.title, type=t.type, tasktype=4, status=1,
                         created_by=GetUser, assigned_to=GetUser, priority=t.priority)
                    crontask.save()
                except:
                    continue

        else:

            #对于周和月处理逻辑， 先判断是否是第一天
            if Is_First_Day(period):

                #如果是第一天， 对于周判断未来7天是否有都是节假日， 如果都是节假日，则继续
                weekisholiday = Is_Holiday(currentweek)
                if period == 'weekday' and weekisholiday:

                    continue

                for u in t.assigned_to.all():
                    try:
                        GetUser = User.objects.get(username=u.username)

                        crontask = Item(title=t.title, type=t.type, tasktype=4, status=1,
                             created_by=GetUser, assigned_to=GetUser, priority=t.priority)
                        crontask.save()
                    except:
                        continue

