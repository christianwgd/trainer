from django.contrib import auth
from django.test import TestCase
from django.urls import reverse
from faker import Faker

from trainer.templatetags.lang_flag_tags import lang_flag
from word.models import Language

User = auth.get_user_model()


class TestTrainerViews(TestCase):

    def setUp(self):
        self.fake = Faker('de_DE')
        self.language_from = Language.objects.create(
            name=self.fake.word(),
            code=self.fake.language_code(),
        )
        self.language_to = Language.objects.create(
            name='Deutsch',
            code='de',
        )
        self.user = User.objects.create_user(
            username=self.fake.user_name(),
        )
        self.user.profile.language = self.language_from
        self.user.profile.learn = self.language_to
        self.user.profile.save()

    def test_index_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_switch_no_user(self):
        response = self.client.get(reverse('switch'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('account_login'))

    def test_switch_user_has_learn_language(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('switch'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_switch_user_has_no_learn_language(self):
        user = User.objects.create_user(
            username=self.fake.user_name(),
        )
        self.client.force_login(user)
        response = self.client.get(reverse('switch'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('userprofile:update'))


class TestLangFlagTags(TestCase):

    def setUp(self):
        self.fake = Faker('de_DE')
        self.language = Language.objects.create(
            name='Deutsch',
            code='de',
        )

    def test_lang_flag_tag(self):
        self.assertEqual(
            lang_flag(self.language),
            f'<img src="/static/flags/{self.language.code}.svg" '
            f'alt="{self.language.name}" class="lang-flag">',
        )
