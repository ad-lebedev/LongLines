from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import ListOfTasks


urlpatterns = [
    url(r'^tasks/$', login_required(ListOfTasks.as_view())),
]
