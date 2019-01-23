from django.db.models.signals import post_save
from django.dispatch import receiver

from quickstart.models import Project, TaskTemplate, Task, SubTask, SubTaskTemplate


@receiver(post_save, sender=Project, dispatch_uid='completing_task')
def completing_task(sender, instance, created, **kwargs):
    print('receiver')
    if not created:
        return
    else:
        for tpl in TaskTemplate.objects.all():
            task = Task.objects.create(project=instance, title=tpl.title, task_type=tpl.task_type)
            for stpl in tpl.subtask_templates.all():
                SubTask.objects.create(task=task, title=stpl.title, department=stpl.department,
                                       days=stpl.days, staff=stpl.staff)


