from django.contrib import auth
from django.test import TestCase
from faker import Faker

from word.models import Language

User = auth.get_user_model()


class UserProfileModelTest(TestCase):

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
