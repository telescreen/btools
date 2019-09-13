from django.contrib import admin
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    """ Company Admin model to allow edit in Admin site """
    list_display = ('quote', 'name', 'industry', 'summary')

admin.site.register(Company, CompanyAdmin)