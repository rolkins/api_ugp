from datetime import date, timedelta

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from rest_framework import viewsets
from quickstart.models import Project, Task, Department, SubTask
from quickstart.serializers import ProjectSerializer, TaskSerializer, DepartmentSerializer, SubTaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        pid = self.request.GET.get('project_id')
        if pid:
            return Task.objects.filter(project_id=pid)
        return Task.objects.all()


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class LoadReportView(View):
    @staticmethod
    def generate(year):
        tasks = Task.objects.filter(start_date__year__lte=year, end_date__year__gte=year)
        result = {}  # {department_id: {project_id: [...months]}}
        departments = {}
        projects = {}
        for task in tasks:
            if task.months == 0:
                continue

            start_month = 0
            end_month = 11
            if task.start_date.year == year:
                start_month = task.start_date.month - 1
            if task.end_date.year == year:
                end_month = task.end_date.month - 1

            for subtask in task.subtasks.all():
                if subtask.department_id not in result:
                    result[subtask.department_id] = {}
                    departments[subtask.department_id] = subtask.department.title
                if task.project_id not in result[subtask.department_id]:
                    result[subtask.department_id][task.project_id] = [0] * 12
                    projects[task.project_id] = task.project.title
                project_row = result[subtask.department_id][task.project_id]
                wdpm = subtask.days * subtask.staff / task.months
                for m in range(start_month, end_month + 1):
                    project_row[m] += wdpm

        for d in result.values():
            for pid in d:
                d[pid] = [round(v, 2) for v in d[pid]]

        return {
            'department_titles': departments,
            'project_titles': projects,
            'data': result,
            'year': year,
        }

    def get(self, request, *args, **kwargs):
        year = int(request.GET.get('year', date.today().year))
        data = self.generate(year)
        if request.GET.get('json') == '1':
            return JsonResponse(data)
        else:
            return render(request, 'report.html', data)

