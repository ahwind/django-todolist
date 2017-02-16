# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Q
from django.db.models import Count
from todo.forms import *
from todo.models import Item, ProjectList, ItemComment
from get_url import GetOrgStructure
import simplejson
import datetime
import xlwt


@login_required(login_url='/login/')
def dashboard(request):

    getnewtask = Item.objects.filter(Q(created_by=request.user) |
                                     Q(assigned_to=request.user)).filter(status=1, is_delete=False)
    base_num = getnewtask.filter(tasktype=1).count()
    business_num = getnewtask.filter(tasktype=2).count()
    pro_num = getnewtask.filter(tasktype=3).count()
    latest = getnewtask.order_by('-created_date')[:10]
    return render(request, 'todo/dashboard.html', locals())


@login_required(login_url='/login/')
def MyToDo(request, stat):

    if request.method == 'POST':

        if 'addtask' in request.POST:

            form = ItemForm(request.POST, initial={'created_by': request.user})

            if form.is_valid():
                try:

                    form.save()
                    messages.success(request, u"一个新的任务被添加.")

                    return HttpResponseRedirect(reverse('mytodo', args=['list']))
                except Exception, e:
                    
                    messages.warning(request,
                                     u"新任务保存有一个问题. "
                                     u"最有可能已经存在在同一组具有相同名称的事项.")
            else:
                messages.warning(request, u'任务添加失败')
                return HttpResponseRedirect(reverse('mytodo', args=['list']))

        elif 'mark_done' in request.POST:
            del_list = request.POST.getlist('mark_done')

            Item.objects.filter(id__in=del_list).update(is_delete=True)
            messages.info(request, u'任务已经删除')

    else:
        form = ItemForm(initial={'created_by': request.user, 'tasktype': 2})

    if stat == 'list':

        latest = Item.objects.filter(tasktype=2, status__in=[1, 2], is_delete=False).filter(
            Q(created_by=request.user) | Q(assigned_to=request.user)).order_by('-created_date')
    else:
        latest = Item.objects.filter(tasktype=2, status__in=[3, 4]).filter(
            Q(created_by=request.user) | Q(assigned_to=request.user)).order_by('-created_date')[:200]
    return render(request, 'todo/todo.html', locals())


@login_required(login_url='/login/')
def CronToDo(request, stat):

    if request.method == 'POST':
        if 'makr_doen' in request.POST:
            del_list = request.POST.getlist('mark_done')

            Item.objects.filter(id__in=del_list).update(is_delete=True)
            messages.info(request, u'任务已经删除')

    if stat == 'list':

        latest = Item.objects.filter(tasktype=4, status__in=[1, 2], is_delete=False).filter(
            Q(created_by=request.user) | Q(assigned_to=request.user)).order_by('-created_date')
    else:
        latest = Item.objects.filter(tasktype=4, status__in=[3, 4]).filter(
            Q(created_by=request.user) |
            Q(assigned_to=request.user)).order_by('-created_date')[:200]
    return render(request, 'todo/todocron.html', locals())


@login_required(login_url='/login/')
def AddProject(request):

    if request.method == 'POST':

        form = ProjectListForm(request.POST, initial={"created_by": request.user})

        if form.is_valid():
            try:
                form.save()
                messages.success(request, u"一个新的事项被添加.")

                return HttpResponseRedirect(reverse('projectlist', args=['list']))
            except Exception, e:
                
                messages.warning(request,
                                 u"新事项保存有一个问题. "
                                 u"最有可能已经存在在同一组具有相同名称的事项.")

    else:
        form = ProjectListForm(initial={"created_by": request.user})
    return render(request, 'todo/baseform.html', locals())


@login_required(login_url='/login/')
def AddBusiness(request):

    if request.method == 'POST':

        form = ItemForm(request.POST, initial={'created_by': request.user})

        if form.is_valid():
            try:

                form.save()
                messages.success(request, u"一个新的事项被添加.")

                return HttpResponseRedirect(reverse('mytodo', args=['list']))
            except Exception, e:
                
                messages.warning(request,
                                 u"新事项保存有一个问题. "
                                 u"最有可能已经存在在同一组具有相同名称的事项.")

    else:
        form = ItemForm(initial={'created_by': request.user, 'tasktype': 2})
    return render(request, 'todo/baseform.html', locals())


@login_required(login_url='/login/')
def AddBaseItem(request):

    if request.method == 'POST':

        form = BaseItemForm(request.POST, initial={'created_by': request.user})

        if form.is_valid():
            try:
                form.save()
                messages.success(request, u"一个新的事项被添加.")
                return HttpResponseRedirect(reverse('baseitemlist'))
            except:
                messages.warning(request,
                                 u"新事项保存有一个问题. 最有可能已经存在在同一组具有相同名称的事项.")

    else:
        form = BaseItemForm(initial={'created_by': request.user})
    return render(request, 'todo/baseform.html', locals())


@login_required(login_url='/login/')
def TaskView(request, pid):

    taskitem = Item.objects.get(pk=pid)

    itemcomment = taskitem.itemcomment_set.all().order_by('-date')

    if request.method == 'POST':
        c = ItemComment(
                author=request.user,
                task=taskitem,
                body=request.POST.get('comment-body', None),
            )
        c.save()

        return HttpResponseRedirect(request.path)

    return render(request, 'todo/taskview.html', locals())


@login_required(login_url='/login/')
def EditTask(request, id):

    GetTask = get_object_or_404(Item, pk=id)

    TaskType = GetTask.tasktype

    if request.method == 'POST':

        if TaskType == 2:
            url = 'mytodo'
            getarg = 'list'

            form = ItemForm(request.POST, instance=GetTask)

        elif TaskType == 1:
            url = 'baseitemlist'
            getarg = 'list'
            form = BaseItemForm(request.POST, instance=GetTask)

        elif TaskType == 3:
            url = 'subprojectlist'
            getarg = GetTask.project.id
            form = EditSubProjectForm(request.POST, instance=GetTask)
        elif TaskType == 4:
            url = 'mycron'
            getarg = 'list'
            form = CronItemForm(request.POST, instance=GetTask)
        else:
            url = 'mytodo'
            messages.warning(request, u'不能识别的任务类型！')
            return HttpResponseRedirect(request.path)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, u"任务修改完成.")
                return HttpResponseRedirect(reverse(url, args=[getarg]))
            except Exception, e:
                
                messages.warning(request,
                               u"任务保存有一个问题. "
                               u"最有可能已经存在在同一组具有相同名称的事项.")

    else:

        if TaskType == 2:
            form = ItemForm(instance=GetTask)
        elif TaskType == 1:
            form = BaseItemForm(instance=GetTask)
        elif TaskType == 3:
            form = EditSubProjectForm(instance=GetTask)
        elif TaskType == 4:
            form = CronItemForm(instance=GetTask)
        else:
            messages.warning(request, u'未知的任务类型')

            return HttpResponseRedirect(reverse('dashboard'))

    return render(request, 'todo/baseform.html', locals())


@login_required(login_url='/login/')
def DelItem(request):

    type = request.GET.get('type')
    itemid = request.GET.get('id')

    if request.method == 'POST':
        if 'mark_doen' in request.POST:
            return HttpResponse(simplejson.dumps(request.POST.getlist('mark_done')))

    if not type or not itemid:
        messages.warning(request, u'参数错误!')
        return HttpResponseRedirect(request.path)

    if type == 'task':
        delitem = get_object_or_404(Item, pk=itemid)
        if delitem.lock:
            return HttpResponse(u'不可以删除绩效锁定的任务，请先删除对应绩效成绩后再联系上级领导处理')
        if not delitem.is_delete:
            delitem.is_delete = True
            delitem.save()
        else:
            delitem.delete()
    elif type == 'pro':
        #delitem = get_object_or_404(ProjectList, pk=itemid)
        pass
    elif type == 'rollback':
        delitem = get_object_or_404(Item, pk=itemid)
        if delitem.tasktype == 3 and delitem.project.stat == 3:

            messages.warning(request, u'父项目已经关闭，无法恢复！')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        if delitem.is_delete:
            delitem.is_delete = False
            delitem.save()

    else:
        messages.warning(request, u'参数错误!')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login/')
def ViewProjectList(request, stat):

    if request.method == 'POST':

        form = ProjectListForm(request.POST, initial = {"created_by": request.user})

        if form.is_valid():
            try:
                form.save()
                messages.success(request, u"一个新的项目被添加.")

                return HttpResponseRedirect(reverse('projectlist'))
            except Exception, e:
                
                messages.warning(request,
                                 u"新项目保存有一个问题. "
                                 u"最有可能已经存在在同一组具有相同名称的项目.")

    else:
        form = ProjectListForm(initial = {"created_by": request.user})

    if stat == 'list':

        if request.user.is_superuser:
            project = ProjectList.objects.filter(stat=1)
        else:

            project = ProjectList.objects.filter(Q(created_by=request.user) | Q(assigned_to__in=[request.user.id]))

    else:
        project = ProjectList.objects.filter(created_by=request.user, stat__in=[2, 3])

    return render(request, 'todo/projectlist.html', locals())


@login_required(login_url='/login/')
def ViewSubProject(request, pid):
    """
    项目列表， 可以创建新项目

    """

    project = ProjectList.objects.get(pk=pid)
    subproject = project.item_set.filter(is_delete=False)
    if request.method == 'POST':
        form = SubProjectForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, u"一个新的任务被添加.")

                return HttpResponseRedirect(reverse('subprojectlist', args=[pid]))
            except Exception, e:

                messages.warning(request,
                               u"新任务保存有一个问题. "
                               u"最有可能已经存在在同一组具有相同名称的事项.")

    else:
        form = SubProjectForm(initial = {"project": project, "created_by": request.user, 'tasktype': 3})
    return render(request, 'todo/subproject.html', locals())


@login_required(login_url='/login/')
def Trashlist(request):
    """
    这里是所有删除任务的列表， 只能做彻底删除和回复操作
    """
    latest = Item.objects.filter(is_delete=True).filter(Q(created_by=request.user) | Q(assigned_to=request.user))
    return render(request, 'todo/trash.html', locals())


@login_required(login_url='/login/')
def BaseItemList(request, stat):

    if request.method == 'POST':

        form = BaseItemForm(request.POST, initial={'created_by': request.user})

        if form.is_valid():
            try:
                form.save()
                messages.success(request, u"一个新的任务被添加.")
                return HttpResponseRedirect(reverse('baseitemlist', args=['list']))
            except Exception, e:
                event = '新任务保存有一个问题: %s' % e
                messages.warning(request, event)

    else:
        form = BaseItemForm(initial={'created_by': request.user, 'status': 3})

    if stat == 'list':
        latest = Item.objects.filter(tasktype=1, is_delete=False, status__in=[1, 2]).filter(
             Q(created_by=request.user) | Q(assigned_to__in=[request.user.id])).order_by('-created_date')[:200]
    else:
        latest = Item.objects.filter(tasktype=1, is_delete=False, status__in=[3, 4]).filter(
             Q(created_by=request.user) | Q(assigned_to__in=[request.user.id])).order_by('-created_date')[:200]
    return render(request, 'todo/todobase.html', locals())


@login_required(login_url='/login/')
def EditProjectList(request, id):
    """
    编辑项目实例

    """

    ProjectItem = get_object_or_404(ProjectList, pk=id)
    if request.method == 'POST':
        form = ProjectListForm(request.POST, instance=ProjectItem)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, u"一个新的任务被添加.")
                return HttpResponseRedirect(reverse('projectlist', args=['list']))
            except Exception, e:
                
                messages.warning(request,
                               u"新任务保存有一个问题. "
                               u"最有可能已经存在在同一组具有相同名称的任务.")

    else:
        form = ProjectListForm(instance=ProjectItem)

        return render(request, 'todo/baseform.html', locals())


@login_required(login_url='/login/')
def Search(request):
    """
    组员工单查看
    """
    if request.method == 'POST':

        qs = []
        tasktype = request.POST.get('tasktype')
        owner = request.POST.getlist('owner')
        startdate = request.POST.get('start_date')
        enddate = request.POST.get('end_date')

        status = request.POST.get('status')

        if tasktype and tasktype != '4':
            qs.append(Q(tasktype=tasktype))

        if status and status != '5':
            qs.append(Q(status=status))

        if owner:
            qs.append(Q(created_by__in=owner) | Q(assigned_to__in=owner))
        else:
            qs.append(Q(created_by=request.user) | Q(assigned_to=request.user))

        if startdate and enddate:
            enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d') + datetime.timedelta(days=1)
            qs.append(Q(created_date__range=(startdate, enddate)))
        else:
            messages.warning(request, u'日期 为必填项')
            return HttpResponseRedirect(reverse('searchlist'))

        q = None

        for x in qs:
            if q:
                q &= x
            else:
                q = x

        if q is None:
            messages.warning(request, u'查询内容不能为空')
            return HttpResponseRedirect(request.path)
        else:
            search_results = Item.objects.filter(q).filter(is_delete=False)
            if not search_results:
                messages.warning(request, u'您的查询没有返回结果')
                return HttpResponseRedirect(reverse('searchlist'))

    else:
        form = SearchForm(initial={'user': request.user.username})
    return render(request, 'todo/search.html', locals())


@login_required(login_url='/login/')
def MyGroup(request):
    """
    管理视图， 用来展示个人和小组当周完成和未完成的任务, 可以导出excel表
    """

    Curr_Week = datetime.date.today().weekday()
    Mon_Date = datetime.date.today() - datetime.timedelta(days=Curr_Week)
    try:
        owner = GetOrgStructure(request.user.username)
        if isinstance(owner, list):
            owneritem = []
            search_results = Item.objects.filter(Q(created_by__username__in=owner) |
                                                 Q(assigned_to__username__in=owner)).filter(
                Q(completed_date__gte=Mon_Date, )|Q(status__in=['1', '2'], is_delete=False)
                ).order_by('-updte_time', 'priority', 'created_date')
        elif owner == 'all':
            search_results = Item.objects.filter(Q(completed_date__gte=Mon_Date, )|
                                                 Q(status__in=['1', '2'], is_delete=False)
                ).order_by('-updte_time', 'priority', 'created_date')
        else:
            search_results = Item.objects.filter(Q(created_by=request.user) |
                                                 Q(assigned_to=request.user)).filter(
                Q(completed_date__gte=Mon_Date, )|Q(status__in=['1', '2'], is_delete=False)
                ).order_by('-updte_time', 'priority', 'created_date')

        if request.method == 'POST':
            if 'export' in request.POST:
                response = HttpResponse(content_type="application/ms-excel")
                response['Content-Disposition'] = 'attachment; filename='+Mon_Date.strftime('%Y%m%d')+'周报.xls'
                wb = xlwt.Workbook()

                ws = wb.add_sheet(u'本周工作完成情况')
                ws.write(0, 0, u'任务')
                ws.write(0, 1, u'创建时间')
                ws.write(0, 2, u'创建人')
                ws.write(0, 3, u'分配给')
                ws.write(0, 4, u'更新时间')
                ws.write(0, 5, u'截止日期')
                ws.write(0, 6, u'权重')
                ws.write(0, 7, u'进度')
                ws.write(0, 8, u'完成情况')

                row = 1
                for i in search_results:
                    created_dt = i.created_date.strftime('%Y-%m-%d')
                    uptime_time = i.updte_time.strftime('%Y-%m-%d %H:%M:%S')
                    if not i.due_date:
                        due_dt = None
                    else:
                        due_dt = i.due_date.strftime('%Y-%m-%d')

                    try:
                        assigned_to = i.assigned_to.username
                    except:
                        assigned_to = ''

                    ws.write(row, 0, i.title)
                    ws.write(row, 1, created_dt)
                    ws.write(row, 2, i.created_by.username)
                    ws.write(row, 3, assigned_to)
                    ws.write(row, 4, uptime_time)
                    ws.write(row, 5, due_dt)
                    ws.write(row, 6, i.get_priority_display())
                    ws.write(row, 7, i.progress)
                    ws.write(row, 8, i.get_status_display())
                    row += 1
                wb.save(response)
                return response

    except:
        messages.warning(request, u'您的帐号没有权限！')

    return render(request, 'todo/mygroup.html', locals())


@login_required(login_url='/login/')
def showgantt(request, gid):
    """
    甘特图展示
    """
    return render(request, 'todo/gantt.html', locals())


@login_required(login_url='/login/')
def TaskStatistics(request):

    Curr_Week = datetime.date.today().weekday()
    Mon_Date = datetime.date.today() - datetime.timedelta(days=Curr_Week)

    CreateNum = User.objects.filter(item_assigned_to__created_date__gte=Mon_Date).annotate(
        task_num=Count('item_assigned_to')).order_by('-task_num')

    ComNum = User.objects.filter(item_assigned_to__created_date__gte=Mon_Date, item_assigned_to__status=3).annotate(
        task_num=Count('item_assigned_to')).order_by('-task_num')

    return render(request, 'todo/statis.html', locals())


@login_required(login_url='/login/')
def MultiAdd(request):

    if request.method == 'POST':

        data = request.POST.copy()
        assigned_to_list = request.POST.getlist('assigned_to')

        for i in assigned_to_list:
            data['assigned_to'] = i
            form = MultiItemForm(data)

            if form.is_valid():
                form.save()

            else:

                event = u'用户%s 分配任务失败' % i
                messages.warning(request, event)

                continue

        return HttpResponseRedirect(reverse('mytodo', args=['list']))
    else:
        form = MultiItemForm(initial={'user': request.user.username, 'created_by': request.user, 'tasktype': 2})

    return render(request, 'todo/baseform.html', locals())


@login_required(login_url='/login/')
def MultiAddCount(request):

    if request.method == 'POST':

        data = request.POST.copy()
        assigned_to_list = request.POST.getlist('assigned_to')

        for i in assigned_to_list:
            data['assigned_to'] = i

            form = MultiCountItemForm(data)

            if form.is_valid():
                form.save()

            else:

                event = u'用户%s 分配任务失败' % i
                messages.warning(request, event)

                continue

        return HttpResponseRedirect(reverse('baseitemlist'))
    else:
        form = MultiCountItemForm(initial={'user': request.user.username, 'created_by': request.user})

    return render(request, 'todo/baseform.html', locals())
