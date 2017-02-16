# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from todo.models import ProjectList, Item,  ParentType, CronTask
from todo.get_url import GetOrgStructure
from django.contrib.auth.models import User
from django.conf import settings

def type_as_group(type):
    program = []

    for p in ParentType.objects.all():
        subprogram = []
        subtype = p.type_set.filter(type=type)
        if subtype.count() != 0:
            for s in subtype:
                subprogram.append((s.id,  s.name))

            program.append((p.name, subprogram))

    return program


class ProjectListForm(ModelForm):

    def __init__(self,  *args, **kwargs):
        super(ProjectListForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ProjectList
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'stat': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple form-control', 'multiple':''}),
            'created_by': forms.HiddenInput(),
        }
        exclude = ('created_date', )


class BaseItemForm(ModelForm):

    def __init__(self,  *args, **kwargs):
        super(BaseItemForm, self).__init__(*args, **kwargs)

        self.fields['type'].widget = forms.Select(attrs={'data-rel': 'chosen'}, choices=type_as_group('count'))

        self.fields['assigned_to'].queryset = User.objects.exclude(username__in=settings.EXCLUDE_USER)

    due_date = forms.DateField(

        required=False,
        widget=forms.DateInput(attrs={'class': 'form_datetime', 'readonly': True}),
        label=u'截止日期',
    )

    class Meta:
        model = Item
        widgets = {
            'created_by': forms.HiddenInput(),
        }
        #fields = ('title', 'type', 'created_by', 'count', 'status')

        exclude = ('is_delete', 'progress', 'lock', 'completed_date', 'project', 'length', 'tasktype')


class CronTaskForm(ModelForm):

    """
    计划类任务设置模板
    """

    def __init__(self,  *args, **kwargs):
        super(CronTaskForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget = forms.Select(choices=type_as_group('count'))

    class Meta:
        model = CronTask
        widgets = {
            'created_by': forms.HiddenInput(),
        }
        fields = '__all__'


class CronItemForm(ModelForm):
    """
    计划类任务实例
    """

    def __init__(self,  *args, **kwargs):
        super(CronItemForm, self).__init__(*args, **kwargs)

        self.fields['type'].widget = forms.Select(choices=type_as_group('count'))

    class Meta:
        model = Item

        fields = ('title', 'type', 'status')


class ItemForm(ModelForm):

    def __init__(self,  *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget = forms.Select(choices=type_as_group('time'))
        self.fields['assigned_to'].queryset = User.objects.exclude(username__in=settings.EXCLUDE_USER)

    due_date = forms.DateField(

        required=False,
        widget=forms.DateInput(attrs={'class': 'form_datetime', 'readonly': True}),
        label=u'截止日期',
    )


    title = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'size': 35}),
        label=u'任务名'
    )

    class Meta:
        model = Item
        widgets = {
            'created_by': forms.HiddenInput(),
            'tasktype': forms.HiddenInput(),
        }
        exclude = ('is_delete', 'progress', 'lock', 'completed_date', 'project', 'count')


class SubProjectForm(ModelForm):
    """
    增加子项目实例Form方法
    """

    def __init__(self,  *args, **kwargs):
        super(SubProjectForm, self).__init__(*args, **kwargs)

        init = kwargs.get('initial')

        if init:
            try:
                pro = init.get('project')
                self.fields['assigned_to'].queryset = pro.assigned_to.all()
            except:
                self.fields['assigned_to'].queryset = init.project.assigned_to.all()


    class Meta:
        model = Item
        widgets = {
            'created_by': forms.HiddenInput(),
            'project': forms.HiddenInput(),
            'tasktype': forms.HiddenInput(),
            'due_date': forms.DateInput(attrs={'class': 'form_datetime'}),


        }
        exclude = ('is_delete', 'lock', 'type', 'completed_date', 'count',)


class MultiItemForm(ModelForm):

    def __init__(self,  *args, **kwargs):
        super(MultiItemForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget = forms.Select(choices=type_as_group('time'))

        init = kwargs.get('initial')

        if init:
            user = init.get('user')
            getuser = GetOrgStructure(user)

            if getuser == 'all':
                c = [(u.id, u.username) for u in  User.objects.exclude(username='admin')]
                self.fields['assigned_to'] = forms.CharField(widget=forms.SelectMultiple(
                    attrs={'class': 'js-example-basic-multiple form-control', 'multiple': ''},
                    choices=c), label=u'选择用户')
            elif isinstance(getuser, list):
                c = [(u.id, u.username) for u in  User.objects.filter(username__in=getuser)]
                self.fields['assigned_to'] = forms.CharField(widget=forms.SelectMultiple(
                    attrs={'class': 'js-example-basic-multiple form-control', 'multiple': ''},
                    choices=c), label=u'选择用户')

        else:
            return



    due_date = forms.DateField(

        required=False,
        widget=forms.DateInput(attrs={'class': 'form_datetime', 'readonly': True}),
        label=u'截止日期',
    )


    class Meta:
        model = Item
        widgets = {
            'created_by': forms.HiddenInput(),
            'tasktype': forms.HiddenInput(),
        }
        exclude = ('is_delete', 'progress', 'lock', 'completed_date', 'project', 'count', )


class MultiCountItemForm(ModelForm):

    def __init__(self,  *args, **kwargs):
        super(MultiCountItemForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget = forms.Select(choices=type_as_group('count'))

        init = kwargs.get('initial')

        if init:
            user = init.get('user')
            getuser = GetOrgStructure(user)

            if getuser == 'all':
                c = [(u.id, u.username) for u in  User.objects.exclude(username='admin')]
                self.fields['assigned_to'] = forms.CharField(widget=forms.SelectMultiple(
                    attrs={'class': 'js-example-basic-multiple form-control', 'multiple': ''},
                    choices=c), label=u'选择用户')
            elif isinstance(getuser, list):
                c = [(u.id, u.username) for u in  User.objects.filter(username__in=getuser)]
                self.fields['assigned_to'] = forms.CharField(widget=forms.SelectMultiple(
                    attrs={'class': 'js-example-basic-multiple form-control', 'multiple': ''},
                    choices=c), label=u'选择用户')

        else:
            return



    due_date = forms.DateField(

        required=False,
        widget=forms.DateInput(attrs={'class': 'form_datetime', 'readonly': True}),
        label=u'截止日期',
    )


    class Meta:
        model = Item
        widgets = {
            'created_by': forms.HiddenInput(),
        }
        exclude = ('is_delete', 'progress', 'lock', 'completed_date', 'project', 'length', 'tasktype' )


class EditSubProjectForm(ModelForm):
    """
    编辑子项目实例Form方法
    """

    def __init__(self,  *args, **kwargs):
        super(EditSubProjectForm, self).__init__(*args, **kwargs)

        ins = kwargs.get('instance')
        self.fields['assigned_to'].queryset = ins.project.assigned_to.all()


    class Meta:
        model = Item
        widgets = {
            'created_by': forms.HiddenInput(),
            'project': forms.HiddenInput(),
            'tasktype': forms.HiddenInput(),
            'due_date': forms.DateInput(attrs={'class': 'form_datetime'}),
        }
        exclude = ('is_delete', 'lock', 'type', 'completed_date', 'count',)


def GetMyGroup(user):

    data = GetOrgStructure(user)

    if data and data == 'all':

        return [(u.id, u.username) for u in  User.objects.exclude(username='admin')]
    elif not data:
        getuser = User.objects.exclude(username=user)
        return
    else:
        return data


class SearchForm(ModelForm):
    """
    搜索表单
    """
    def __init__(self, *args, **kwargs):

        super(SearchForm, self).__init__(*args, **kwargs)

        init = kwargs.get('initial')

        if init:
            user = init.get('user')
            getuser = GetOrgStructure(user)

            if getuser == 'all':
                c = [(u.id, u.username) for u in  User.objects.exclude(username='admin')]
                self.fields['owner'] = forms.CharField(widget=forms.SelectMultiple(
                    attrs={'class': 'js-example-basic-multiple form-control', 'multiple': ''},
                    choices=c), label=u'选择查询用户')
            elif isinstance(getuser, list):
                c = [(u.id, u.username) for u in  User.objects.filter(username__in=getuser)]
                self.fields['owner'] = forms.CharField(widget=forms.SelectMultiple(
                    attrs={'class': 'js-example-basic-multiple form-control', 'multiple': ''},
                    choices=c), label=u'选择查询用户')

        else:
            return

        STATUS_CHOICES = (

            (1, (u'未开始')),
            (2, (u'进行中')),
            (3, (u'已完成')),
            (4, (u'已关闭')),
            (5, ('ALL')),
        )

        TASK_TYPE = (

            (1, (u'基本任务')),
            (2, (u'下发任务')),
            (3, (u'项目任务')),
            (4, ('ALL')),
        )

        self.fields['tasktype'].widget = forms.Select(attrs={'class': 'form-control'}, choices=TASK_TYPE)
        self.fields['status'].widget = forms.Select(attrs={'class': 'form-control'}, choices=STATUS_CHOICES)
        self.fields['start_date'] = forms.DateField(widget=forms.TextInput(attrs={'class': 'form_datetime'}),
                                                    label=u'开始时间', help_text=' *'
                                                    )
        self.fields['end_date'] = forms.DateField(widget=forms.TextInput(attrs={'class': 'form_datetime'}),
                                                  label=u'结束时间', help_text=' *')


    class Meta:

        model = Item

        fields = ('tasktype', 'status',)