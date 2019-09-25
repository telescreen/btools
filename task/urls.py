""" Path pattern for /task-manage """

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='task-index'),
]
