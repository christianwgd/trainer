from django.contrib import auth
from django.test import TestCase
from django.urls import reverse
from faker import Faker

from word.models import Language

User = auth.get_user_model()


class TestTrainerViews(TestCase):

    def setUp(self):
        self.fake = Faker('de_DE')
        self.language_from = Language.objects.create(
            name=self.fake.word(),
            code=self.fake.language_code()
        )
        self.language_to = Language.objects.create(
            name='Deutsch',
            code='de'
        )
        self.user = User.objects.create_user(
            username=self.fake.user_name(),
        )
        self.user.profile.language = self.language_from
        self.user.profile.learn = self.language_to
        self.user.profile.save()
        self.client.force_login(self.user)

    def test_index_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
