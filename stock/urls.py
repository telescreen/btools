""" Path pattern for /stock """

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='stock-index'),
    path('company/<int:stock_quote>/', views.company_detail, name='stock-company-detail'),
    path('company/upload', views.upload_company, name='stock-company-upload')
]
