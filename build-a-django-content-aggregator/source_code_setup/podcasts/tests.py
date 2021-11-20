from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
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

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse('home_page'))
        self.assertTemplateUsed(response, 'homepage.html')

    def test_home_page_contains_correct_content(self):
        response = self.client.get(reverse('home_page'))
        self.assertContains(response, 'Preparing to launch my portfolio')