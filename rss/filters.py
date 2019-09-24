""" Allow users to filter rss feeds """

import django_filters
from .models import Feed


class FeedFilter(django_filters.FilterSet):
    """ Feed Filter """
    class Meta:
        model = Feed
        fields = ['checked']
