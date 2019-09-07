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
    """ Routinely fetch feeds from remote sources """
    logger.info('--- Start to fetch new feed ---')
    all_sources = Source.objects.all()
    for source in all_sources:
        logger.info('etag=%s, modified=%s', source.etag, source.modified)
        feeds = feedparser.parse(source.url, modified=source.modified, etag=source.etag)

        # Status != 304 means that there are new feeds
        if feeds.status == 200:
            logger.info('--- Fetching %s ---', source.url)
            for entry in feeds.entries:
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

                # Only insert the feed if feed does not already exist.
                if not Feed.objects.filter(feed_id=entry.id).exists():
                    new_feed = Feed(title=entry.title, link=entry.link, feed_id=entry.id,
                                    content=entry.summary, author=entry.author,
                                    created_at=published, updated_at=published, source=source)
                    # This function commit a entry everytime it parses
                    # This might affects performance in production environment with lots of feeds.
                    new_feed.save()

            # Update etag and modified
            source.etag = feeds.etag
            source.modified = feeds.modified
            source.save()

            logger.info('Update etag and modified. etag=%s, modified=%s', feeds.etag, feeds.modified)
            logger.info('Done processing all new entries for %s', source.url)

        elif feeds.status == 304:
            logger.info('Skipping %s because of no new entries', source.url)

        else:
            logger.error('Error while processing %s', source.url)
