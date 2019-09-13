""" Path pattern for /stock """

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='stock-index'),
    path('fetch', views.fetch),
    path('upload/company', views.upload_company, name='stock-upload-company')
]
