""" API implementations """
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# --- Views ---
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'task/task-index.html')


def project_detail(request: HttpRequest, project_name: str) -> HttpResponse:
    return render(request, 'task/task-index.html')
