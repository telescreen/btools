""" Path pattern for /stock """

from django.urls import path

from . import views

urlpatterns = [
    path('', views.company_list, name='stock-index'),
    path('company/<int:stock_quote>/', views.company_detail, name='stock-company-detail'),
    path('company/<int:stock_quote>/data', views.fetch_data),
    path('company/upload', views.upload_company, name='stock-company-upload')
]
