# Celery Tasks to Fetch contents and parse Feeds

import logging
import time
import feedparser

from celery import shared_task
from .models import Feed, Source

# Get an instance of a logger
logger = logging.getLogger(__name__)

@shared_task
def fetch_feed():
    logger.info('--- Start to fetch new feed ---')
    all_sources = Source.objects.all()
    for source in all_sources:
        d = feedparser.parse(source.url, etag=source.etag, modified=source.modified)

        # Status != 304 means that there are new feeds
        if d.status == 200:
            logger.info("--- Fetching {} ---".format(source.url))
            for entry in d.entries:
                # Datetime parsed among RSS version is ntot
                try:
                    published = entry.published_parsed
                except AttributeError:
                    try:
                        published = entry.updated_parsed
                    except AttributeError:
                        published = entry.created_parsed
                # Convert datetime back to string to store to database
                if isinstance(published, time.struct_time):
                    published = time.strftime('%Y-%m-%dT%H:%M:%S%z', published)
                else:
                    published = published.strftime('%Y-%m-%dT%H:%M:%S%z')

                f = Feed(title=entry.title, link=entry.link, feed_id=entry.id,
                         content=entry.summary, author=entry.author,
                         updated_at=published, source=source)
                # This function commit a entry everytime it parses
                # This might affects performance in production environment with lots of feeds.
                f.save()
            # Update etag and modified
            logger.info('Update etag and modified. etag={}, modified={}'.format(d.etag, d.modified))
            source.etag = d.etag
            source.modified = d.modified
            source.save()
            logger.info('Done processing all new entries')

        elif d.status == 304:
            logger.info('Skipping because of no new entries')

        else:
            logger.error('Error while processing {}'.format(source.url))