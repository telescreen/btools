from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='rss-index'),
    path('category/add', views.category_add, name='rss-category-add'),
    path('source/add', views.source_add, name='rss-source-add'),
]
