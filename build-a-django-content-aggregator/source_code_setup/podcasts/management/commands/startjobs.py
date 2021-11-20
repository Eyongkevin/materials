from django.core.management.base import BaseCommand
import feedparser
from dateutil import parser
from podcasts.models import Episode
from typing import Any, Optional

RSS_CONTAINER  = {}

def register_rss(rss):
    RSS_CONTAINER[rss.__name__] = rss
    return rss

def save_new_feeds(feed):
    podcast_title = feed.channel.title
    podcast_image = feed.channel.image["href"]

    for item in feed.entries:
        if not Episode.objects.filter(guid=item.guid).exists():
            episode = Episode(
                title=item.title,
                description=item.description,
                pub_date=parser.parse(item.published),
                link=item.link,
                image=podcast_image,
                podcast_name=podcast_title,
                guid=item.guid,
            )
            episode.save()

@register_rss
def real_python_rss():
    _feed = feedparser.parse("https://realpython.com/podcasts/rpp/feed")
    save_new_feeds(_feed)

@register_rss
def talk_python_rss():
    _feed = feedparser.parse("https://talkpython.fm/episodes/rss")
    save_new_feeds(_feed)

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        for rss in RSS_CONTAINER:
            RSS_CONTAINER[rss]()
        