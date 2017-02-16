#coding: utf-8
from todo.models import ProjectList
from django.shortcuts import HttpResponse
import simplejson

def get_list_gantt(request):
    if request.GET.get('gid'):
        Group_Id = request.GET.get('gid', None)
        Get_List = ProjectList.objects.get(pk=Group_Id)
        Get_Item = Get_List.item_set.filter(is_delete=False)
        List_Item = [{'id': i.id,
                      'title': i.title,
                      'status': i.get_status_display(),
                      'created_date': i.created_date.strftime("%m/%d/%Y"),
                      'update_time': i.updte_time.strftime("%m/%d/%Y"),
                      'assigned_to': i.assigned_to.username,
                      'progress': i.progress} for i in Get_Item]


        return HttpResponse(simplejson.dumps(List_Item))
    return HttpResponse('ok')
