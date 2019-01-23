from rest_framework import serializers
from quickstart.models import Project, Task, Department, SubTask


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'created', 'title', 'start_date', 'end_date', 'project_done')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'title')


class SubTaskSerializer(serializers.ModelSerializer):
    department_title = serializers.CharField(read_only=True, source='department.title')
    task_type = serializers.IntegerField(read_only=True, source='task.task_type')

    class Meta:
        model = SubTask
        fields = ('id', 'title', 'department_title', 'department', 'done', 'staff', 'days', 'task', 'task_type')


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = ('id', 'project', 'title', 'start_date', 'end_date', 'task_type', 'subtasks')
