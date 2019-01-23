from django.contrib import admin
from .models import Project, Task, Department, TaskTemplate, SubTaskTemplate, SubTask


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 0


class SubTaskTemplateInline(admin.TabularInline):
    model = SubTaskTemplate
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = 'project',
    inlines = SubTaskInline,


@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    inlines = SubTaskTemplateInline,


admin.site.register(Department)
admin.site.register(Project)
