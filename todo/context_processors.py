# -*- coding: utf-8 -*-
from todo.models import Item


def box(request):

    #baseitem = Item.objects.filter(status=1, is_delete=False).filter(assigned_to=request.user)
    if request.user.is_active:
        todoitem = Item.objects.filter(status=1, is_delete=False).filter(assigned_to=request.user).count()
        countitem = Item.objects.filter(status=1, is_delete=False).filter(assigned_to=request.user).filter(tasktype=1).count()
        clockitem = Item.objects.filter(status=1, is_delete=False).filter(assigned_to=request.user).filter(tasktype=2).count()
        proitem = Item.objects.filter(status=1, is_delete=False).filter(assigned_to=request.user).filter(tasktype=3).count()
        cronitem = Item.objects.filter(status=1, is_delete=False).filter(assigned_to=request.user).filter(tasktype=4).count()
    else:

        todoitem = countitem = clockitem = proitem = cronitem = 0
        #return HttpResponse(u'好像哪里出错了, 请联系管理员处理。')

    return {'unclock': clockitem, 'unpro': proitem, 'uncron': cronitem, 'unall': todoitem, 'uncount': countitem}
