""" Path pattern for /utils """

from django.urls import path

from . import views

urlpatterns = [
    path('hash/', views.index, name='hash-index'),
]
