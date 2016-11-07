# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.decorators import register
from django import forms

from .models import LearningGroup, TaskList, Task, TaskProgress


class AdminAudit(admin.ModelAdmin):
    class Meta:
        abstract = True

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
        obj.save()


class AdminForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Task
        fields = ['name', 'description']


@register(LearningGroup)
class LearningGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ['students']
    list_filter = ['tutor']
    list_display = ('name', 'tutor', 'date_started', 'is_active')


@register(Task)
class TaskAdmin(AdminAudit):
    form = AdminForm
    list_display = ('number', 'name', 'author')
    list_filter = ['author']
    ordering = ('author', 'number')


@register(TaskList)
class TaskListAdmin(AdminAudit):
    list_display = ('name', 'author')
    list_filter = ['author']
    ordering = ('author',)
    fields = ('name', 'description', 'tasks')
    filter_horizontal = ['tasks']


@register(TaskProgress)
class TaskProgressAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'task_status', 'created_date', 'changed_date')
    list_filter = ['task', 'student', 'task_status']
