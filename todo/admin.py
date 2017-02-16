#coding:utf-8

from django.contrib import admin
from todo.models import Type, ParentType, CronTask
from todo.forms import CronTaskForm

class ParentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'base', 'value', 'type')
    ordering = ['parent']
    search_fields = ('name', 'parent__name',)


class CronTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'created_by', 'period', 'priority', 'is_active',)
    search_fields = ('title',)
    filter_horizontal = ('assigned_to', )

    form = CronTaskForm

    def save_model(self, request, obj, form, change):

        obj.created_by = request.user
        obj.save()


admin.site.register(CronTask, CronTaskAdmin)
admin.site.register(ParentType, ParentTypeAdmin)
admin.site.register(Type, TypeAdmin)
