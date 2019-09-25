
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from rest_framework import viewsets

from .models import Project, ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'task-index.html')
