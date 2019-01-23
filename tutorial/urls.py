from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from quickstart.views import ProjectViewSet, TaskViewSet, DepartmentViewSet, SubTaskViewSet, LoadReportView

router = DefaultRouter()
router.register(r'project', ProjectViewSet)
router.register(r'task', TaskViewSet, base_name="task_list")
router.register(r'subtask', SubTaskViewSet)
router.register(r'department', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^ugp/', include(router.urls)),
    url(r'^report/$', LoadReportView.as_view()),
]
