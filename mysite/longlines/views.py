from django.views.generic import ListView
from . import models


class ListOfTasks(ListView):
    model = models.Task
