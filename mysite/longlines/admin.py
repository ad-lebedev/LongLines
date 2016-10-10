from django.contrib import admin
from .models import LearningGroup


class LearningGroupAdmin(admin.ModelAdmin):
    fields = ('name', 'date_started')
    list_display = ('name', 'tutor', 'date_started')

admin.site.register(LearningGroup, LearningGroupAdmin)
