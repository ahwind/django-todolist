# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from todo.sendmail import Notification
from todo.senddata import SendTodoData
from decimal import Decimal
import datetime


class ParentType(models.Model):


    name = models.CharField(u'名称', max_length=100)

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = u'父级分类'
        verbose_name_plural = verbose_name


class Type(models.Model):

    TYPE_CHOICES = (
        ('time', u'耗时'),
        ('count', u'计次'),
    )

    name = models.CharField(u'名称', max_length=40)
    base = models.DecimalField(u'KPI基本分',
                                max_digits=5,
                                 decimal_places=2,
                                 default=1.00,
                                 blank=True,
                                 null=True)

    value = models.DecimalField(u'难度系数',
                                max_digits=5,
                                 decimal_places=3,
                                 default=1.00,
                                 blank=True,
                                 null=True)
    type = models.CharField(u'类型', max_length=5, choices=TYPE_CHOICES, default='count')
    parent = models.ForeignKey(ParentType, verbose_name=u'父级', default=1)

    def getvalue(self):

        return self.base * self.value

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = u'绩效分类'
        verbose_name_plural = verbose_name

class Holidays(models.Model):

    date = models.DateField(u'日期')
class CronTask(models.Model):

    PRIORITY_CHOICES = (
        (1, u'紧急'),
        (2, u'重要'),
        (3, u'高'),
        (4, u'正常'),
        (5, u'低'),
    )

    PERIOD_CHOICES = (
        ('day', u'每日'),
        ('weekday', u'每周'),
        ('month', u'每月'),
        ('quarter', u'每季'),
    )
    title = models.CharField(u'任务名', max_length=140)
    type = models.ForeignKey(Type, verbose_name=u'业务类型', blank=True, null=True)
    period = models.CharField(u'任务周期', choices=PERIOD_CHOICES, default='day', max_length=10)
    created_by = models.ForeignKey(User, related_name='cron_created_by', verbose_name=u'创建人', blank=True, null=True)
    assigned_to = models.ManyToManyField(User, verbose_name=u'分配给')
    note = models.TextField(u'备注', blank=True)
    priority = models.IntegerField(
        (u'权重'),
        choices=PRIORITY_CHOICES,
        default=4,
        blank=3,
        help_text=(u'1 = 最高权重, 5 = 最低权重'),
        )
    is_active = models.BooleanField(u'有效', default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'计划任务'
        verbose_name_plural = verbose_name


class ProjectList(models.Model):

    STATUS_CHOICES = (
        (1, u'进行中'),
        (2, u'已完成'),
        (3, u'已关闭'),
    )

    name = models.CharField(u'事项名', max_length=60)
    created_date = models.DateField(u'创建日期', auto_now=True)
    created_by = models.ForeignKey(User, related_name='list_created_by', verbose_name=u'创建者')
    assigned_to = models.ManyToManyField(User, related_name='list_assigned_to', verbose_name=u'分配给')
    stat = models.IntegerField(
        (u'状态'),
        choices=STATUS_CHOICES,
        default=1,
        )

    def getsubnum(self):
        try:
            return self.item_set.filter(is_delete=False).count()
        except:
            return 0


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = u'项目列表'
        verbose_name_plural = verbose_name


class Item(models.Model):

    STATUS_CHOICES = (
        (1, u'未开始'),
        (2, u'进行中'),
        (3, u'已完成'),
        (4, u'已关闭'),
    )

    PRIORITY_CHOICES = (
        (1, u'紧急'),
        (2, u'重要'),
        (3, u'高'),
        (4, u'正常'),
        (5, u'低'),
    )


    TASK_TYPE = (
        (1, u'基本任务'),
        (2, u'待办任务'),
        (3, u'项目任务'),
        (4, u'定期任务'),
    )
    title = models.CharField(u'任务名', max_length=140)
    project = models.ForeignKey(ProjectList, verbose_name=u'项目名称', blank=True, null=True)
    type = models.ForeignKey(Type, verbose_name=u'业务类型', blank=True, null=True)
    tasktype = models.IntegerField(
        (u'任务类型'),
        choices=TASK_TYPE,
        default=1,
    )

    created_date = models.DateTimeField(u'创建时间', blank=True, null=True, auto_now_add=True)
    #start_time = models.DateTimeField(u'任务开始时间', blank=True, null=True)
    updte_time = models.DateTimeField(u'更新时间', auto_now=True)
    due_date = models.DateField(u'截止日期', blank=True, null=True)
    progress = models.CharField(u'进度', blank=True, max_length=3, default='0', help_text=u'输入100内数值')
    length = models.DecimalField(u'持续时间',
                                max_digits=5,
                                decimal_places=3,
                                default=1,
                                blank=True,
                                null=True,
                                help_text=u'小时 此为默认值，非说明不要修改')
    count = models.IntegerField(u'次数', blank=True, null=True, default=1)
    status = models.IntegerField(
        (u'任务状态'),
        choices=STATUS_CHOICES,
        default=1,
    )
    #extra_stat -1： 未分配 0：正常  1：垃圾箱
    is_delete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(u'完成日期', blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='item_created_by', verbose_name=u'创建人')
    assigned_to = models.ForeignKey(User, related_name='item_assigned_to',
                                    verbose_name=u'分配给', blank=True, null=True)
    note = models.TextField(u'备注', blank=True)
    priority = models.IntegerField(
        (u'权重'),
        choices=PRIORITY_CHOICES,
        default=4,
        blank=3,
        help_text=(u'1 = 最高权重, 5 = 最低权重'),
        )

    #锁定后无法修改截至日期，无法删除
    lock = models.BooleanField(default=False) #False 正常 True 锁定


    def _get_status(self):
        """
        Displays the ticket status
        """
        return u'%s' % (self.get_status_display())
    get_status = property(_get_status)

    def _get_priority(self):
        return u'%s' % (self.get_priority_display())
    get_priority = property(_get_priority)

    def overdue_status(self):
        """
        返回是否逾期
        :return:
        """
        if self.due_date and self.status in [1,2] and datetime.date.today() > self.due_date:
            return True

    def com_due_status(self):

        if self.due_date and self.completed_date > self.due_date:
            return True

    def per_value(self):
        try:
            if self.tasktype == 3:
                perfvalue = self.length

            else:
                perfvalue = Decimal(str(self.type.base)) * Decimal(str(self.type.value)) * \
                            Decimal(str(self.length)) * Decimal(str(self.count))


            return perfvalue
        except:
            return 0

    def __unicode__(self):
        return '%s' % self.title

    # Auto-set the item creation / completed date
    def save(self):

        """
        如果状态为3（完成）且未锁定， 修改为锁定
        """

        if self.created_by and not self.assigned_to:
            self.assigned_to = self.created_by

        if self.status == 3 and not self.lock:
            self.completed_date = datetime.datetime.now()
            self.lock = True
            self.progress = '100'

            try:
                if self.tasktype == 3:
                    perfvalue = self.length
                    type = 'pro'
                else:
                    perfvalue = Decimal(str(self.type.base)) * Decimal(str(self.type.value)) * \
                                Decimal(str(self.length)) * Decimal(str(self.count))
                    type = 'base'

                try:
                    owner = self.assigned_to.username
                except:
                    owner = self.created_by.username
              
                result = SendTodoData(title=self.title, value=perfvalue, owner=owner, type=type)
                if not result:
                    raise Exception('Error')
            except Exception, e:
                raise Exception('Error from source %s' % e)

        if self.status == 1 and self.tasktype != 1:
            a = Notification(u'您有新的任务需要处理')

            msg = u'任务: %s <br><br>' \
                  u'创建人: %s<br><br>' \
                  u'<a href="http://todo.example.com/">详细信息请访问任务管理系统</a><br>' % \
                  (self.title, self.created_by.username)
            try:
                sender = self.assigned_to.username
            except:
                sender = self.task.created_by.username

            a.send_email(sender, msg)


        super(Item, self).save()


    class Meta:
        ordering = ["priority"]
        verbose_name = u'任务'
        verbose_name_plural = verbose_name


class ItemComment(models.Model):
    """
    Not using Django's built-in comments because we want to be able to save
    a comment and change task details at the same time. Rolling our own since it's easy.
    """
    author = models.ForeignKey(User)
    task = models.ForeignKey(Item)
    date = models.DateTimeField(default=datetime.datetime.now)
    body = models.TextField(blank=True)
    reply = models.ForeignKey('self', verbose_name=u'上级评论', blank=True, null=True, related_name='parent_comment')

    def __unicode__(self):
        return '%s - %s' % (
            self.author,
            self.date,
        )
    class Meta:
        verbose_name = u'评论'
        verbose_name_plural = verbose_name

    def save(self):

        a = Notification(u'您有新的评论')

        msg = u'任务: %s <br><br>' \
              u'评论人: %s<br><br>' \
              u'内容: %s <br><br>' \
              u'<a href="http://todo.example.com/">详细信息请访问任务管理系统</a><br>' % \
              (self.task.title, self.author.username, self.body)
        try:
            sender = self.task.assigned_to.username
        except:
            sender = self.task.created_by.username

        a.send_email(sender, msg)
        super(ItemComment, self).save()


