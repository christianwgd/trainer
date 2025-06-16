from django.contrib import auth
from django.test import TestCase
from django.utils.translation import gettext as _
from faker import Faker

from word.forms import WordForm
from word.models import Word, Language


User = auth.get_user_model()


class WordBaseTest(TestCase):

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


class TestWordModel(WordBaseTest):

    def setUp(self):
        super().setUp()

    def test_string_representation(self):
        self.assertEqual(str(self.word), self.word.source)

    def test_string_representation_language(self):
        self.assertEqual(str(self.language_from), self.language_from.name)
        self.assertEqual(str(self.language_to), self.language_to.name)


class TestWordForms(WordBaseTest):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username=self.fake.user_name(),
        )

    def test_word_form_valid(self):
        data = {
            'source': self.fake.word(),
            'translation': self.fake.word(),
        }
        form = WordForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_word_form_invalid(self):
        data = {}
        form = WordForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),2)
