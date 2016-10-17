from django.contrib import admin
from .models import LearningGroup, TaskList, Task
from django import forms
# from django.contrib.auth.models import User
# from django.db.models import Q


# class LearningGroupAdminForm(forms.ModelForm):
#     class Meta:
#         model = LearningGroup
#
#     def __init__(self, *args, **kwargs):
#         super(LearningGroupAdminForm, self).__init__(*args, **kwargs)
#         if 'students' in self.initial:
#             self.fields['students'].queryset = User.objects.filter(Q(is_active=True))
#             self.fields['students'].queryset = User.objects.filter(Q(Active=True) | Q(group__=date.today()))


class LearningGroupAdmin(admin.ModelAdmin):
    # form = LearningGroupAdminForm
    filter_horizontal = ['students']
    list_filter = ['tutor']
    list_display = ('name', 'tutor', 'date_started', 'is_active')


class TaskAdminFrom(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Task
        fields = ['name', 'description']


class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminFrom

    list_filter = ['name', 'author']
    list_display = ('number', 'name', 'author')
    ordering = ('author', 'number')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
        obj.save()


class TaskListAdmin(admin.ModelAdmin):
    filter_horizontal = ['tasks']
    # list_filter = ['tasks']
    fields = ['name']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.username
        obj.save()


admin.site.register(TaskList, TaskListAdmin)
admin.site.register(LearningGroup, LearningGroupAdmin)
admin.site.register(Task, TaskAdmin)
