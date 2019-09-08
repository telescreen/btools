""" Path pattern for /hash """

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='hash-index'),
]
