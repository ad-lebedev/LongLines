from django.conf.urls import url
from .views import ListOfTasks


urlpatterns = [
    url(r'^tasks/$', ListOfTasks.as_view()),
]
