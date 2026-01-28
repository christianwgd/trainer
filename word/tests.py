import pytest
from django.contrib import auth
from django.core import serializers
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from faker import Faker

from word.forms import WordCreateForm, WordQueryForm
from word.models import Language, Word
from word.templatetags.index_tags import get_item

User = auth.get_user_model()


class WordBaseTest(TestCase):

    def setUp(self):
        self.fake = Faker('de_DE')
        self.language_from = Language.objects.create(
            name=_('German'),
            code='de',
        )
        self.language_to = Language.objects.create(
            name=_('Italian'),
            code='it',
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
        self.user.profile.learn = self.language_to
        self.user.profile.save()

    def test_word_form_init(self):
        form = WordCreateForm(user=self.user)
        self.assertEqual(form.fields['source'].label, self.user.profile.learn)
        self.assertEqual(form.fields['translation'].label, self.user.profile.language)

    def test_word_form_valid(self):
        data = {
            'source': self.fake.word(),
            'translation': self.fake.word(),
        }
        form = WordCreateForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['source'], data['source'])
        self.assertEqual(form.cleaned_data['translation'], data['translation'])

    def test_word_form_invalid(self):
        data = {}
        form = WordCreateForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),2)

    def test_word_form_double(self):
        data = {
            'source': self.word.source,
            'translation': self.word.translation,
        }
        form = WordCreateForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),1)
        self.assertIn(_('This word already exists.'), form.errors['source'])

    def test_word_query_form_valid(self):
        data = {
            'query_string': self.fake.word(),
            'language': self.user.profile.language.code,
        }
        form = WordQueryForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['query_string'], data['query_string'])
        self.assertEqual(form.cleaned_data['language'], data['language'])


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
            set(response.context['translate']),
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
            'from_lang': self.user.profile.language.code,
            'to_lang': self.user.profile.learn.code,
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

    def test_word_query_view_get(self):
        response = self.client.get(reverse('word:query'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'word/word_query.html')

    def test_word_query_view_get_with_session(self):
        word_json = serializers.serialize("json", Word.objects.all())
        sess = self.client.session
        sess.update({'query_result': word_json})
        sess.save()
        response = self.client.get(reverse('word:query'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'word/word_query.html')
        self.assertIn(self.word.source, response.content.decode())
        self.assertIn(self.word.translation, response.content.decode())

    def test_word_query_view_post(self):
        test_word = Word.objects.create(
            source=self.fake.word(),
            translation=self.fake.word(),
            from_lang=self.language_from,
            to_lang=self.language_to,
        )
        word_json = serializers.serialize("json", Word.objects.all())
        sess = self.client.session
        sess.update({'query_result': word_json})
        sess.save()
        data = {
            'query_string': test_word.translation,
            'language': test_word.from_lang.code,
        }
        response = self.client.post(reverse('word:query'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('word:query'))

    def test_word_query_view_post_reverse(self):
        test_word = Word.objects.create(
            source=self.fake.word(),
            translation=self.fake.word(),
            from_lang=self.language_from,
            to_lang=self.language_to,
        )
        word_json = serializers.serialize("json", Word.objects.all())
        sess = self.client.session
        sess.update({'query_result': word_json})
        sess.save()
        data = {
            'query_string': test_word.translation,
            'language': test_word.to_lang.code,
        }
        response = self.client.post(reverse('word:query'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('word:query'))


class TestIndexTags(TestCase):

    def test_get_item(self):
        my_list = ['apple', 'banana', 'cherry']
        self.assertEqual(get_item(0, my_list), 'apple')
        self.assertEqual(get_item(1, my_list), 'banana')
        self.assertEqual(get_item(2, my_list), 'cherry')
        with pytest.raises(IndexError):
            get_item(3, my_list)  # Should raise IndexError for out of range index
