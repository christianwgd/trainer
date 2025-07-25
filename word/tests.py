from django.contrib import auth
from django.test import TestCase
from django.urls import reverse
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
        self.user.profile.language = self.language_from
        self.user.profile.save()

    def test_word_form_init(self):
        form = WordForm(user=self.user)
        self.assertEqual(form.fields['source'].label, self.user.profile.learn)
        self.assertEqual(form.fields['translation'].label, self.user.profile.language)

    def test_word_form_valid(self):
        data = {
            'source': self.fake.word(),
            'translation': self.fake.word(),
        }
        form = WordForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['source'], data['source'])
        self.assertEqual(form.cleaned_data['translation'], data['translation'])

    def test_word_form_invalid(self):
        data = {}
        form = WordForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),2)

    def test_word_form_double(self):
        data = {
            'source': self.word.source,
            'translation': self.word.translation,
        }
        form = WordForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),1)
        self.assertIn(_('This word already exists.'), form.errors['source'])


class TestWordViews(WordBaseTest):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username=self.fake.user_name(),
        )
        self.user.profile.language = self.language_from
        self.user.profile.learn = self.language_to
        self.user.profile.save()
        self.client.force_login(self.user)

    def test_word_list_view(self):
        response = self.client.get(reverse('word:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'word/word_list.html')
        self.assertFalse(response.context['reverse'])

    def test_word_reverse_view(self):
        response = self.client.get(reverse('word:reverse'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'word/word_list.html')
        self.assertTrue(response.context['reverse'])

    def test_word_pair_list_view(self):
        response = self.client.get(reverse('word:pairs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'word/word_pairs.html')
        self.assertEqual(
            set(response.context['word_list']),
            set(response.context['translate'])
        )

    def test_word_pair_list_view_reverse(self):
        response = self.client.get(reverse('word:pairs_reverse'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'word/word_pairs.html')

    def test_word_create_view_get(self):
        response = self.client.get(reverse('word:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'word/word_form.html')

    def test_word_create_view_post(self):
        data = {
            'source': self.fake.word(),
            'translation': self.fake.word(),
            'from_lang': self.user.profile.language,
            'to_lang': self.user.profile.learn,
        }
        response = self.client.post(reverse('word:create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('word:create'))

    def test_word_update_view_get(self):
        response = self.client.get(reverse('word:update', args=[self.word.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'word/word_form.html')

    def test_word_update_view_post(self):
        data = {
            'source': self.fake.word(),
            'translation': self.fake.word(),
        }
        response = self.client.post(reverse('word:update', args=[self.word.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_word_ignore_view(self):
        response = self.client.get(reverse('word:ignore', args=[self.word.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.word, self.user.profile.exclude.all())
