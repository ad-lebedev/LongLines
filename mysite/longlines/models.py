import datetime

from django.db import models
from django.contrib.auth.models import User


class ModelAudit(models.Model):
    author = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    @property
    def created_by_user(self):
        return User.objects.get(username=self.author)


class Task(ModelAudit):
    number = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=1000)

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'


class TaskList(ModelAudit):
    tasks = models.ManyToManyField(
        Task,
        through='TaskTaskList',
        through_fields=('task_list', 'task')
    )


class TaskTaskList(models.Model):
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    task_number = models.PositiveSmallIntegerField()


class LearningGroup(models.Model):
    name = models.CharField(max_length=10)
    date_started = models.DateField()
    task_list = models.ForeignKey(TaskList, on_delete=models.DO_NOTHING, blank=True, null=True)
    tutor = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='tutors',
        related_query_name='tutor',
        limit_choices_to={'is_active': True})

    def limit_students_from_users():
        return {'groups__name__contains': 'students'}

    students = models.ManyToManyField(
        User,
        related_name='students',
        limit_choices_to=limit_students_from_users)

    def is_active(self):

        now_date = datetime.date.today()
        now_month = now_date.month
        if now_month <= 6:
            active_year = now_date.year - 1
        else:
            active_year = now_date.year
        now_date = now_date.replace(year=active_year, month=9, day=1)
        return self.date_started >= now_date
    is_active.admin_order_field = 'date_started'
    is_active.boolean = True
    is_active.short_description = 'Is active?'

    def __str__(self):
        return self.name


class TaskProgress(models.Model):
    status_choices = (
        (1, 'New'),
        (2, 'Sent to check'),
        (3, 'Passed'),
        (4, 'Declined')
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    task_status = models.PositiveSmallIntegerField(verbose_name='status', choices=status_choices)
    created_date = models.DateTimeField()
    changed_date = models.DateTimeField()


class Parameters(models.Model):
    circuit_diargam_choices = (
        (1, 'Open circuit'),
        (2, 'Short circuit'),
        (3, 'Resistance'),
        (4, 'Capacitance'),
        (5, 'Parallel res/cap'),
        (6, 'Series res/cap'),
        (7, 'Inductance'),
        (8, 'Parallel res/ind'),
        (9, 'Series res/ind'),
    )
    task = models.ForeignKey(TaskProgress, on_delete=models.CASCADE)
    date_published = models.DateTimeField()
    circuit_diagram_type = models.PositiveSmallIntegerField(choices=circuit_diargam_choices)
    R_gen = models.PositiveSmallIntegerField()
    U_gen = models.PositiveSmallIntegerField(default=1000)
    T_gen = models.PositiveSmallIntegerField(verbose_name='pulse time')
    L_line = models.PositiveSmallIntegerField(verbose_name='length')
    X_line = models.PositiveSmallIntegerField(verbose_name='position')
    T_line = models.PositiveSmallIntegerField()
    Ro_line = models.PositiveSmallIntegerField()
    R_load = models.PositiveSmallIntegerField()
    L_load = models.PositiveSmallIntegerField()
    C_load = models.PositiveSmallIntegerField()
    T_delay_osc = models.PositiveSmallIntegerField(verbose_name='delay')
    T_sweep_osc = models.PositiveSmallIntegerField(verbose_name='sweep')
    comment = models.CharField(max_length=500)
