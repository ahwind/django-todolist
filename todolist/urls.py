from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^login/$', 'todolist.login.login_view'),
    url(r'^accounts/logout/$', 'todolist.login.Logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'todo.views.dashboard', name="dashboard"),
    url(r'^todo/(?P<stat>done|list)/$', 'todo.views.MyToDo', name="mytodo"),
    url(r'^cron/(?P<stat>done|list)/$', 'todo.views.CronToDo', name="mycron"),
    #add task and project
    url(r'^todo/add/$', 'todo.views.AddBusiness', name="addbusinesstask"),
    url(r'^base/add/$', 'todo.views.AddBaseItem', name="addbaseitem"),
    url(r'^todo/(?P<pid>\d+)$', 'todo.views.TaskView', name="taskview"),
    # add project
    url(r'^project/add/$', 'todo.views.AddProject', name="addproject"),
    url(r'^project/edit/(?P<id>\d+)/$', 'todo.views.EditProjectList', name="editproject"),
    url(r'^project/(?P<stat>done|list)/$', 'todo.views.ViewProjectList', name="projectlist"),
    url(r'^project/(?P<pid>\d+)/$', 'todo.views.ViewSubProject', name="subprojectlist"),
    #url(r'^project/(?P<pid>\d+)/add/$', 'todo.views.AddSubProject', name="addsubproject"),
    url(r'^task/edit/(?P<id>\d+)/$', 'todo.views.EditTask', name="edittaskitem"),
    #
    url(r'^base/(?P<stat>list|done)/$', 'todo.views.BaseItemList', name='baseitemlist'),
    url(r'^delitem/$', 'todo.views.DelItem', name='delitem'),
    url(r'^trash/$', 'todo.views.Trashlist', name='trashlist'),
    url(r'^mygroup/$', 'todo.views.MyGroup', name='mygroup'),
    url(r'^search/$', 'todo.views.Search', name='searchlist'),
    url(r'^todo/multi/clock/$', 'todo.views.MultiAdd', name='multiaddtask'),
    url(r'^todo/multi/count/$', 'todo.views.MultiAddCount', name='multiaddtaskcount'),
    #gant
    url(r'^ganttapi/$', 'todo.gantt.get_list_gantt'),
    url(r'^gantt/(?P<gid>\d+)/$', 'todo.views.showgantt', name='gantt'),
    #statistics
    url(r'^statistics/$', 'todo.views.TaskStatistics', name='taskstatistics'),

]

#handler403 = 'todo.views.page_forbidden'
#handler404 = 'todo.views.page_not_found'
#handler500 = 'todo.views.page_error'

