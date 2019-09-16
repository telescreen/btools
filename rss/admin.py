""" Expose Model for Django Admin Page """

from django.contrib import admin

from .models import Source, Category
# Register your models here.
admin.site.register(Source)
admin.site.register(Category)
