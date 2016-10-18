from django.contrib import admin
from .models import LearningGroup, TaskList, Task
from django import forms


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


class LearningGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ['students']
    list_filter = ['tutor']
    list_display = ('name', 'tutor', 'date_started', 'is_active')


class TaskAdmin(AdminAudit):
    form = AdminForm
    list_display = ('number', 'name', 'author')
    list_filter = ['author']
    ordering = ('author', 'number')


class TaskListAdmin(AdminAudit):
    list_display = ('name', 'author')
    list_filter = ['author']
    ordering = ('author',)
    fields = ('name', 'description', 'tasks')
    filter_horizontal = ['tasks']


admin.site.register(TaskList, TaskListAdmin)
admin.site.register(LearningGroup, LearningGroupAdmin)
admin.site.register(Task, TaskAdmin)
