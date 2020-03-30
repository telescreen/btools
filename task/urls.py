""" Path pattern for /task-manage """

from django.urls import path

from . import views
from . import api

urlpatterns = [
    path('', views.index, name='task-index'),
    path('projects/<project_name>', views.project_detail,
         name='task-project-detail'),
    path('api/projects/', api.ProjectListView.as_view()),
    path('api/projects/<pk>/', api.ProjectDetailView.as_view()),
    path('api/tasks/', api.TaskView.as_view()),
]
