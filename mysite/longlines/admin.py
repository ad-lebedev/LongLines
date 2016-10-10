from django.contrib import admin
from .models import LearningGroup


class LearningGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ['students']
    list_filter = ['students']

admin.site.register(LearningGroup, LearningGroupAdmin)
