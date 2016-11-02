import datetime

from django.db import models
from django.contrib.auth.models import User


class ModelAudit(models.Model):
    author = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='')

    class Meta:
        abstract = True

    @property
    def created_by_user(self):
        try:
            user = User.objects.get(username=self.username)
        except User.DoesNotExists:
            user = None
        except User.MultipleObjectsReturned:
            user = User.objects.filter(username=self.username).first()
        finally:
            return user

    @created_by_user.setter
    def created_by_user(self, user):
        self.author = user.username


class Task(ModelAudit):
    number = models.PositiveSmallIntegerField(blank=True)

    def save(self):
        if self._state.adding:
            self.number = Task.objects.filter(author=self.author).count() + 1
        super(Task, self).save()

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.name


class TaskList(ModelAudit):
    tasks = models.ManyToManyField(
        Task,
        related_name='task_lists',
        related_query_name='task_list',
        # Как определить limit_choises_to для этого случая?
        # Нужно ограничить выбор только задачами, созданными
        # тем же пользователем, который создает данный тасклист. - на уровне формы. модельная форма, атрибут модел, указываем модель
        # дальше отпределяем свойства полей формы. formfield model selection multiple
    )

    def __str__(self):
        return self.name

    def save(self):
        super(TaskList, self).save()
        qt = TaskList.objects.get(pk=self.pk).tasks.all()
        qg = LearningGroup.objects.filter(task_list_id=self.pk)
        if qt.count() != 0 and qg.count != 0:
            print(qt.count())
            print(qg.count())


def limit_students_from_users():
    return {
            # 'learning_group_student__name__isnull': True,
            'is_active': True,
            'groups__name__contains': 'students'}


class LearningGroup(models.Model):
    # Главный вопрос: как при сохранении учебной группы, когда ей назначает преподаватель ТаскЛист,
    # делать записи в таблице TaskProgress, для всех студентов из этой группы, со стасом Новая
    # метод save - был ли назначен тасклист ил был изменен
    # if not self._state.adding and (
    #         self.creator_id != self._loaded_values['creator_id']):
    #     raise ValueError("Updating the value of creator isn't allowed")
    # super(...).save(*args, **kwargs)
    # https://docs.djangoproject.com/en/1.10/ref/models/instances/#customizing-model-loading
    # создание таск прогресса - на уровне таск листа. метод можем вызвать после сохранения учебной группы.
    # один метод - по списку сдудентов создает таск прогрессы
    # второй - получает после сохранения список студентов и вызывает первый метод

    name = models.CharField(max_length=50)
    date_started = models.DateField()
    # Преподаватель должен указывать ссылку на задание для группы. Но в списке доступных должен видеть только свое. - на уровне view
    task_list = models.ForeignKey(TaskList, on_delete=models.DO_NOTHING, blank=True, null=True)
    # группы назначаются преподавателю, и преподаватель должен иметь возможность назначать конкретной группе задание (тасклист).
    tutor = models.ForeignKey(
        User,
        related_name='learning_group_tutors',
        related_query_name='learning_group_tutor',
        limit_choices_to={'groups__name__contains': 'tutors'}
    )

    students = models.ManyToManyField(
        User,
        related_name='learning_group_students',
        related_query_name='learning_group_student',
        # При таком фильтре, как указан ниже, уже указанные в других группах студенты не только
        # не попадают в список доступных, но и не отображаются в списке уже выбранных...
        # Есть ли возможность ограничить список выбора студентов для группы только не указанными ни в одной группе,
        # но принадлежащие Auth группе, содержащей имя Студенты
        limit_choices_to=limit_students_from_users
    )

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

    # def save(self):
    #     super(LearningGroup, self).save()
    #     TaskList.create_task_progress(self.task_list, self.students.all())


class TaskProgress(models.Model):
    status_choices = (
        (1, 'Новая'),
        (2, 'Ожидает проверки'),
        (3, 'Выполнено'),
        (4, 'Отклонено')
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    task_status = models.PositiveSmallIntegerField(verbose_name='status', choices=status_choices)
    created_date = models.DateTimeField().auto_now_add
    changed_date = models.DateTimeField().auto_now
    student = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='task_progress_student',
    )


class Parameters(models.Model):
    circuit_diargam_choices = (
        (1, 'Холостой ход'),
        (2, 'Короткое замыкание'),
        (3, 'Резистивная нагрузка'),
        (4, 'Емкостная нагрузка'),
        (5, 'Параллельное соединение резистор/конденсатор'),
        (6, 'Последовательное соединение резистор/конденсатор'),
        (7, 'Индуктивная нагрузка'),
        (8, 'Параллельное соединение резистор/катушка'),
        (9, 'Последовательное соединение резистор/катушка'),
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
