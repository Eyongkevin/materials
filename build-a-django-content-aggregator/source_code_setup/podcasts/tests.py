from django.test import TestCase
from django.utils import timezone
from .models import Episode

# Create your tests here.
class PodCastsTests(TestCase):
    def setUp(self) -> None:
        self.episode = Episode.objects.create(
            title="My Podcast Episode",
            description="Preparing to launch my portfolio",
            pub_date = timezone.now(),
            link = "https://codewithenow.com",
            image="https://image.codewithenow.com",
            podcast_name = "My First Podcast with Python/Django",
            guid = "ZmP8JpW6cfLMWyiT2PTPMt4E-K84y0o8SI3z5JGKya0"
        )

    def test_episode_content(self):
        self.assertEqual(self.episode.title, "My Podcast Episode")
        self.assertEqual(self.episode.description, "Preparing to launch my portfolio")
        self.assertEqual(self.episode.link, "https://codewithenow.com")

    def test_episode_str_representation(self):
        self.assertEqual(
            str(self.episode), "My First Podcast with Python/Django: My Podcast Episode"
        )