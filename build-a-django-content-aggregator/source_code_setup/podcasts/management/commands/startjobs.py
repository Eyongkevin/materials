from datetime import timezone
from django.core.management.base import BaseCommand
import feedparser
from dateutil import parser
from podcasts.models import Episode
from typing import Any, Optional

import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler # scheduler to run jobs
from apscheduler.triggers.cron import CronTrigger # a type of trigger
from django_apscheduler.models import DjangoJobExecution # used to run the cleanup 
from django_apscheduler.jobstores import DjangoJobStore  # Determine how jobs are stored


logger = logging.getLogger(__name__)
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

def delete_old_job_executions(max_age = 604_800):
    '""Delete all apscheduler job execition logs older than amax_age'
    DjangoJobExecution.ojbects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        for rss in RSS_CONTAINER:
            scheduler.add_job(
                RSS_CONTAINER[rss],
                trigger='interval',
                minutes=2,
                id=rss,
                max_instances=1,
                replace_existing=True,
            )
            logger.info(f"Added job: {rss}")
        
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week='mon', hour='00', minute='00'
            ), # Midnight on Monday, before start of the next work week
            id='Delete Old Job Execution',
            max_instances=1,
            replace_existing=True,
        ),
        logger.info('Added weekly job: Delete old Job Execution')
        
        try:
            logger.info('Starting scheduler...')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Stopping scheduler...'),
            scheduler.shutdown()
            logger.info('Scheduler shut down successfully!')