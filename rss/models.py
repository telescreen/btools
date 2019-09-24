""" models for RSS apps """

from django.db import models


class Category(models.Model):
    """ Category model """
    name = models.CharField(max_length=200, default='Default Category')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Source(models.Model):
    """ A source represents a RSS url. A source can only belong to a category."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200)
    interval = models.IntegerField(default=1440)
    etag = models.CharField(max_length=100, null=True)
    modified = models.CharField(max_length=100, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<Source {}>".format(self.name)


class Feed(models.Model):
    """ A feed represents content delivered from source at a specific moment."""
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    link = models.CharField(max_length=1000)
    feed_id = models.CharField(max_length=1000, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    checked = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return '<Feed {}>'.format(self.title)
