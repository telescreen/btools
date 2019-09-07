""" View functions for /rss path """

import logging
from datetime import datetime
import feedparser

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

from .forms import CategoryForm, SourceForm
from .models import Category, Source, Feed


# Get an instance of a logger
logger = logging.getLogger(__name__)
NUMBER_OF_FEEDS_PERPAGE = 50


def index(request):
    """ Display a news menu. Return all categories and static page to load feeds asynchronously """
    categories = Category.objects.all()
    category_form = CategoryForm()
    source_form = SourceForm()
    return render(request, 'rss/rss.html', {
        'categories': categories,
        'source_form': source_form,
        'category_form': category_form})


def load_feeds(request, source_name=None):
    """ Return feed results for a source through ajax """
    # We will get the feed of the first source to display
    result = {}
    if source_name is not None:
        feeds = Feed.objects\
                    .filter(source__name=source_name)\
                    .order_by('-created_at')[:NUMBER_OF_FEEDS_PERPAGE]
        result['feeds'] = []
        for feed in feeds:
            result['feeds'].append({
                'id': feed.id,
                'title': feed.title,
                'content': feed.content,
                'author': feed.author,
                'checked': feed.checked,
                'created_at': feed.created_at.strftime('%a %l:%m%p')
            })
        result['size'] = feeds.count()
        result['status_code'] = 200
    return JsonResponse(result)


def update_feed(request):
    """ Update feed metadata """
    userdata = request.POST.copy()
    checked = True if userdata.get('checked') == "true" else False
    feed_id = userdata.get('feed_id')
    feed = Feed.objects.filter(pk=feed_id).first()

    if feed:
        feed.checked = checked
        feed.updated_at = datetime.now()
        feed.save()
        return JsonResponse({'status_code': 200, 'message': 'Successfully updated feed {}'.format(feed_id)})
    else:
        return JsonResponse({'status_code': 404, 'message': 'Feed not found'}, status=404)


def category_add(request):
    """ Add a new rss category """
    if request.method == 'POST':
        # Process with adding category
        form = CategoryForm(request.POST)
        category_existed = Category.objects.filter(name=form.data.get('name')).exists()
        if form.is_valid() and not category_existed:
            logger.debug('Adding a category to database %s', form.cleaned_data)
            form.save()
            messages.success(request, 'Category successfully added')
        else:
            messages.error(request, 'Could not create category. Category might already existed')
        return redirect('/rss/')



def source_add(request):
    """ Add a new rss source """
    update_interval = {'hourly': 1, 'daily': 24, 'weekly': 168, 'monthly': 672}

    if request.method == 'POST':
        # Process with adding category
        form = SourceForm(request.POST)
        if form.is_valid():
            logger.debug('Adding a source to database %s', form.cleaned_data)
            source = form.save(commit=False)

            # Following metadata will be parsed from Feed.s
            psource = feedparser.parse(source.url)
            source.name = psource.channel.title
            source.description = psource.channel.description
            source.interval = int(psource.channel.sy_updatefrequency) * update_interval[psource.channel.sy_updateperiod]

            source.save()
            messages.success(request, 'Source successfully added')
        return redirect('/rss/')