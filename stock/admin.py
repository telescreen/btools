""" Expose model to Django Admin Page """

from django.contrib import admin
from .models import Company, DailyStockPrice


class CompanyAdmin(admin.ModelAdmin):
    """ Company Admin model to allow edit in Admin site """
    list_display = ('quote', 'name', 'industry', 'summary')


class DailyStockPriceAdmin(admin.ModelAdmin):
    """ Daily Stock Price information in Admin site """
    list_display = ('quote', 'date', 'open_price', 'high_price', 'low_price',
                    'close_price', 'volume', 'adjusted_price')

admin.site.register(Company, CompanyAdmin)
admin.site.register(DailyStockPrice, DailyStockPriceAdmin)
