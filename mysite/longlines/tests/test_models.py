# coding=utf-8
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from mixer.backend.django import mixer

from longlines.models import TaskList, LearningGroup, TaskProgress


class LongLinesModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(LongLinesModelTestCase, cls).setUpClass()
        cls.student_one = get_user_model().objects.create_user(
            username='student_1', password='password_1')
        cls.student_two = get_user_model().objects.create_user(
            username='student_2', password='password_2')
        cls.students = [cls.student_one, cls.student_two]

        cls.tutor = get_user_model().objects.create_user(
            username='tutor', password='tutor')

        cls.tasks = mixer.cycle(3).blend('longlines.Task')
        cls.task_list = TaskList.objects.create(name='List')

        for t in cls.tasks:
            cls.task_list.tasks.add(t)
        cls.task_list.save()

        cls.learning_group = LearningGroup.objects.create(
            name='LearningGroup',
            task_list=cls.task_list,
            date_started=datetime.now().date(),
            tutor=cls.tutor)

        cls.learning_group.students.add(cls.student_one)
        cls.learning_group.students.add(cls.student_two)
        cls.learning_group.save()

    def test_create_task_progresses_method(self):
        self.assertEqual(TaskProgress.objects.count(), 0)

        with self.assertRaises(ValueError):
            self.task_list.create_task_progresses({})

        self.task_list.create_task_progresses(self.students)
        self.assertEqual(TaskProgress.objects.count(), 6)

        self.task_list.create_task_progresses(self.students)
        self.assertEqual(TaskProgress.objects.count(), 6)

    def test_get_students_list_method(self):
        students_list = list(self.task_list.get_students_list())
        self.assertEqual(isinstance(students_list, list), True)
