from datetime import date

from django.db import models
from django.db.models import Sum, F
from django.utils.functional import cached_property


class Project(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=300)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    project_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Task(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=300)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    task_type = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @cached_property
    def months(self):
        if self.start_date is None or self.end_date is None:
            return 0
        i = 0
        d = date(self.start_date.year, self.start_date.month, 1)
        while d <= self.end_date:
            i += 1
            try:
                d = date(d.year, d.month+1, 1)
            except ValueError:
                d = date(d.year+1, 1, 1)
        return i


class SubTask(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='subtasks')
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=300)
    done = models.BooleanField(default=False)
    staff = models.PositiveIntegerField(default=0)
    days = models.PositiveIntegerField(default=0)


class Department(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class TaskTemplate(models.Model):
    title = models.CharField(max_length=300, blank=True, default='Задача')
    task_type = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class SubTaskTemplate(models.Model):
    task_template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name='subtask_templates')
    title = models.CharField(max_length=300, blank=True, default='Подзадача')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subtask_templates')
    days = models.PositiveIntegerField(default=0)
    staff = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
