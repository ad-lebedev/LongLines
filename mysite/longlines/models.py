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
    def __str__(self):
        return self.name

class task(ModelAudit):
    number = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=1000)

class task_list(ModelAudit):
    tasks = models.ManyToManyField(
        task,
        through='task_task_list',
        through_fields=('task_list', 'task')
    )

class task_task_list(models.Model):
    task_list = models.ForeignKey(task_list, on_delete=models.CASCADE)
    task = models.ForeignKey(task, on_delete=models.CASCADE)
    task_number = models.PositiveSmallIntegerField()

class learning_group(models.Model):
    name = models.CharField(max_length=10)
    date_started = models.DateField()
    task_list = models.ForeignKey(task, on_delete=models.CASCADE)
    tutor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tutors',
        related_query_name='tutor',
        limit_choices_to={'is_active': True})
    student = models.ManyToManyField(
        User,
        through='learning_group_members',
        through_fields=('group', 'student')
    )

class learning_group_members(models.Model):
    group = models.ForeignKey(learning_group, on_delete=models.CASCADE)
    student = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

class task_progress(models.Model):
    status_choices = (
        (1, 'New'),
        (2, 'Sent to check'),
        (3, 'Passed'),
        (4, 'Declined')
    )
    task = models.ForeignKey(task, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    task_status = models.PositiveSmallIntegerField(verbose_name='status', choices=status_choices)
    created_date = models.DateTimeField()
    changed_date = models.DateTimeField()

class parameters(models.Model):
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
    task = models.ForeignKey(task_progress, on_delete=models.CASCADE)
    date_published = models.DateTimeField()
    circuit_diagram_type = models.PositiveSmallIntegerField(choices=diargam_choices)
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
