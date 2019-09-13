""" Views for /scraper application """

import os
import csv

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings

from .forms import CompanyDataUploadForm
from .models import Company

def index(request):
    """ Return a view to this application """
    companies = Company.objects.all()

    return render(request, 'index.html', {'companies': companies})


def fetch(request):
    """ Return html content for an URL """
    url = request.GET['url']
    result = {}

    r = requests.get(url)
    if r.status_code == 200:
        result['text'] = r.text
        result['status_code'] = 200
    else:
        result['status_code'] = r.status_code
        result['text'] = ''

    return JsonResponse(result)


def upload_company(request):
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
            with open(path, 'r') as destination:
                # read csv
                csv_reader = csv.reader(destination)
                if form.cleaned_data.get('has_header'):
                    next(csv_reader)    # Ignore header

                for row in csv_reader:
                    if not Company.objects.filter(quote=row[2]).exists():
                        company = Company(name=row[1], quote=row[2], industry=row[3], summary=row[4])
                        company.save()
            return redirect('stock-index')
    else:
        form = CompanyDataUploadForm()
    return render(request, 'upload_company.html', {'form': form})