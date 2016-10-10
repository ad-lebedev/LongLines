from django.contrib import admin
from .models import LearningGroup, TaskList
# from django import forms
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
    list_filter = ['date_started', 'tutor']
    list_display = ('name', 'tutor', 'date_started', 'is_active')


class TaskListAdmin(admin.ModelAdmin):
    filter_horizontal = ['tasks']
    list_filter = ['tasks']


admin.site.register(TaskList, TaskListAdmin)
admin.site.register(LearningGroup, LearningGroupAdmin)
