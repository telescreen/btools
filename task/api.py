from rest_framework import generics
from rest_framework import mixins
from .models import (
    Project,
    Task,
    ProjectListSerializer,
    ProjectSerializer,
    TaskSerializer
)


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.order_by('id')
    serializer_class = ProjectListSerializer


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskView(generics.RetrieveUpdateDestroyAPIView,
               mixins.CreateModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
