""" Path pattern for /rss """

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='rss-index'),
    path('loadcategories', views.load_categories),
    path('loadfeeds/<source_name>', views.load_feeds),
    path('updatefeed', views.update_feed),
    path('category/add', views.category_add, name='rss-category-add'),
    path('source/add', views.source_add, name='rss-source-add'),
]
