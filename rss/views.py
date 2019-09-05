import logging
import feedparser

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.contrib import messages

from .forms import CategoryForm, SourceForm
from .models import Category, Source


# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    categories = Category.objects.order_by('name').all()
    return render(request, 'rss/index.html', {'categories': categories})


def category_add(request):
    categories = Category.objects.order_by('name').all()
    if request.method == 'POST':
        # Process with adding category
        form = CategoryForm(request.POST)
        if form.is_valid():
            logger.debug("Adding a category to database {}".format(form.cleaned_data))
            form.save()
            messages.success(request, 'Category successfully added')
    else:
        form = CategoryForm()
    return render(request, "rss/category_add.html", {'form': form, 'categories': categories})


def source_add(request):
    update_interval = {'hourly': 1, 'daily': 24, 'weekly': 168, 'monthly': 672}
    categories = Category.objects.order_by('name').all()

    if request.method == 'POST':
        # Process with adding category
        form = SourceForm(request.POST)
        if form.is_valid():
            logger.debug("Adding a source to database {}".format(form.cleaned_data))
            source = form.save(commit=False)

            # Following metadata will be parsed from Feed.s
            psource = feedparser.parse(source.url)
            source.name = psource.channel.title
            source.description = psource.channel.description
            source.interval = int(psource.channel.sy_updatefrequency) * update_interval[psource.channel.sy_updateperiod]

            source.save()
            messages.success(request, 'Source successfully added')
    else:
        form = SourceForm()
    return render(request, "rss/source_add.html", {'form': form, 'categories': categories})
