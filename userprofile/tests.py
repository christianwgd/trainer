from django.contrib import auth
from django.test import TestCase
from django.urls import reverse
from faker import Faker

from word.models import Language

User = auth.get_user_model()


class UserProfileTest(TestCase):

    def setUp(self):
        self.fake = Faker('de_DE')
        self.lang = Language.objects.create(code='de')
        self.user = User.objects.create(
            username=self.fake.user_name(),
        )

    def test_profile_created(self):
        self.assertIsNotNone(self.user.profile)

    def test_profile_str(self):
        self.assertEqual(str(self.user.profile), self.user.username)

    def test_profile_update_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('userprofile:update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/userprofile_form.html')

    def test_profile_update_view_post(self):
        self.client.force_login(self.user)
        data = {
            'language': self.lang.id,
            'learn': self.lang.id,
        }
        response = self.client.post(reverse('userprofile:update'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.language, self.lang)
        self.assertEqual(self.user.profile.learn, self.lang)
