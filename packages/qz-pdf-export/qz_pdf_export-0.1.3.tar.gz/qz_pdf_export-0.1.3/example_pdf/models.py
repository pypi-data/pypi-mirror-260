from django.db import models


# Create your models here.
class TodoType(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '待办类型'
        verbose_name_plural = verbose_name


class TodoItem(models.Model):
    title = models.CharField(max_length=255, verbose_name='标题')
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name='副标题')
    sys_name = models.CharField(max_length=100, verbose_name='系统名称', default='')
    # client_id = models.CharField(max_length=100, verbose_name='系统Client ID')
    todo_uid = models.CharField(max_length=100, unique=True, verbose_name='待办UID')
    redirect_url = models.URLField(verbose_name='待办跳转URL')
    assignee = models.CharField(max_length=255, verbose_name='待办人')
    assignee_id = models.CharField(max_length=100, verbose_name='待办人ID')
    initiator = models.CharField(max_length=255, blank=True, null=True, verbose_name='发起人')
    initiator_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='发起人ID')
    handler = models.CharField(max_length=255, blank=True, null=True, verbose_name='经办人')
    handler_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='经办人ID')
    reminder_count = models.IntegerField(default=0, verbose_name='催办次数')
    notes = models.TextField(blank=True, null=True, verbose_name='备注')
    is_completed = models.BooleanField(default=False, verbose_name='已完成状态')
    completion_time = models.DateTimeField(blank=True, null=True, verbose_name='办结时间')
    completer = models.CharField(max_length=255, blank=True, null=True, verbose_name='办结人')
    completer_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='办结人ID')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    due_date = models.DateField(blank=True, null=True, verbose_name='截止日期')  # 添加截止日期字段
    type = models.ForeignKey(TodoType, on_delete=models.CASCADE, blank=True, null=True, verbose_name='类型')

    class Meta:
        verbose_name = '待办事项'
        verbose_name_plural = '待办事项'

    def __str__(self):
        return self.title
