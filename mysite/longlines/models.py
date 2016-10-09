from django.db import models
from django.contrib.auth.models import User


class ModelAudit(models.Model):
    author = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    @property
    def created_by_user(self):
        return User.objects.get(username=self.author)


class Task(ModelAudit):
    number = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=1000)


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
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    tutor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tutors',
        related_query_name='tutor',
        limit_choices_to={'is_active': True})
    student = models.ManyToManyField(
        User,
        through='LearningGroupMembers',
        through_fields=('group', 'student')
    )


class LearningGroupMembers(models.Model):
    group = models.ForeignKey(LearningGroup, on_delete=models.CASCADE)
    student = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)


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
    diargam_choices = (
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
    circuit_diagram_type = models.PositiveSmallIntegerField(choices=diargam_choices)
    R_gen = models.PositiveSmallIntegerField()
    U_gen = models.PositiveSmallIntegerField(default=1000)
    T_gen = models.PositiveSmallIntegerField('pulse time')
    L_line = models.PositiveSmallIntegerField('length')
    X_line = models.PositiveSmallIntegerField('position')
    T_line = models.PositiveSmallIntegerField()
    Ro_line = models.PositiveSmallIntegerField()
    R_load = models.PositiveSmallIntegerField()
    L_load = models.PositiveSmallIntegerField()
    C_load = models.PositiveSmallIntegerField()
    T_delay_osc = models.PositiveSmallIntegerField('delay')
    T_sweep_osc = models.PositiveSmallIntegerField('sweep')
    comment = models.CharField(max_length=500)
