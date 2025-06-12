from django.test import TestCase
from django.utils.translation import gettext as _
from faker import Faker

from word.models import Word, Language


class TestWordModel(TestCase):

    def setUp(self):
        self.fake = Faker('de_DE')
        self.language_from = Language.objects.create(
            name=self.fake.word(),
            code=self.fake.language_code()
        )
        self.language_to = Language.objects.create(
            name=_('German'),
            code='de'
        )
        self.word = Word.objects.create(
            source=self.fake.word(),
            translation=self.fake.word(),
            from_lang=self.language_from,
            to_lang=self.language_to,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.word), self.word.source)

    def test_string_representation_language(self):
        self.assertEqual(str(self.language_from), self.language_from.name)
        self.assertEqual(str(self.language_to), self.language_to.name)
