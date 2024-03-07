from django.contrib import admin

from example_pdf.models import TodoItem, TodoType
from pdfExport.admin import PdfAdmin


# Register your models here.

@admin.register(TodoItem)
class TodoItemAdminBase(PdfAdmin):
    list_display = ('title', 'assignee', 'created_at', 'updated_at', 'is_completed', 'pdf_show')
    list_filter = ('created_at', 'updated_at', 'assignee')
    search_fields = ('title', 'assignee')
    # pdf要显示的字段
    pdf_fields = (('组标题', {('title', 'assignee')}), 'handler', ('时间', {('created_at',)}), 'type')
    # pdf标题
    pdf_title = '策略申请表'
    # 要显示所有选项的字段
    option_fields = ['type', ]
    # 左右上方小标题
    left_tip = '编号AAA'
    right_tip = '编号BBB'
    # 如有其他需求，可以自定义pdf_template，继承base_pdf_template.html，添加需要的模块


@admin.register(TodoType)
class TodoTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
