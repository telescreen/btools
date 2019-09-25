""" Views for /scraper application """

import os
import csv
import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, Http404, JsonResponse
from django.conf import settings
from django.core.paginator import Paginator
import django_tables2 as tables

from .forms import CompanyDataUploadForm
from .models import Company, DailyStockPrice, StockTimeStamp

COMPANY_PER_PAGE = 20

# Get an instance of a logger
logger = logging.getLogger(__name__) # pylint: disable=invalid-name


class CompanyTable(tables.Table):
    class Meta:
        model = Company
        exclude = ('id', )
        attrs = {'class': 'table table-sm'}


def company_list(request: HttpRequest) -> HttpResponse:
    """ Return a view to this application """
    companies = Company.objects.all()
    table = CompanyTable(companies)
    table.paginate(page=request.GET.get("page", 1), per_page=COMPANY_PER_PAGE)

    return render(request, 'company_list.html', {'table': table})


def company_detail(request, stock_quote: int) -> HttpResponse:
    """ Return a view to Company details """
    try:
        company = Company.objects.get(quote=str(stock_quote))
        # TODO(me): Implement company detail view logic
    except Company.DoesNotExist:
        raise Http404("Company with releated quote does not exist")
    return render(request, 'company_detail.html', { 'company': company })



def fetch_data(request: HttpRequest) -> JsonResponse:
    """ Load data for stock quote """
    stock_quote: str = request.GET.get('quote', None)
    start_date: str = request.GET.get('sd', '')
    end_date: str = request.GET.get('ed', '')

    result = {}

    if stock_quote:
        company = Company.objects.filter(quote=stock_quote).first()
        if company:
            pass


def upload_company(request: HttpRequest) -> HttpResponse:
    """ Upload all company information from CSV """
    if request.method == 'POST':
        # Processing Request
        form = CompanyDataUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved. by binary
            uploaded_file = request.FILES['file']
            path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # open csv
            with open(path, 'rb') as destination:
                csv_reader = csv.reader(destination)
                if form.cleaned_data.get('has_header'):
                    next(csv_reader)    # Ignore header

                for row in csv_reader:
                    try:
                        if not Company.objects.filter(quote=row[2]).exists():
                            company = Company(name=row[1], quote=row[2],
                                              industry=row[3], summary=row[4])
                            company.save()
                    except IndexError:
                        logger.info('Line %s has format error', csv_reader.line_num)
            return redirect('stock-index')
    else:
        form = CompanyDataUploadForm()
    return render(request, 'upload_company.html', {'form': form})
