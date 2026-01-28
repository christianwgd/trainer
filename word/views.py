from random import shuffle

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, FormView, ListView, UpdateView

from word.forms import WordCreateForm, WordQueryForm, WordUpdateForm
from word.models import Word


class WordListView(LoginRequiredMixin, ListView):
    model = Word

    def get_queryset(self):
        amount = self.request.user.profile.list_amount
        exclude = self.request.user.profile.exclude.values_list('id', flat=True)
        return Word.objects.exclude(id__in=exclude).random(min(amount, Word.objects.count()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.path.endswith('reverse/'):
            context['reverse'] = True
        else:
            context['reverse'] = False
        return context


class WordPairListView(LoginRequiredMixin, ListView):
    model = Word
    template_name = 'word/word_pairs.html'
    queryset = Word.objects.none()

    def get_queryset(self):
        amount = self.request.user.profile.pair_amount
        exclude = self.request.user.profile.exclude.values_list('id', flat=True)
        words = Word.objects.exclude(id__in=exclude).random(amount)
        self.queryset = words
        return words

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs_copy = list(self.queryset)
        shuffle(qs_copy)
        context['translate'] = qs_copy
        if self.request.path.endswith('reverse/'):
            context['reverse'] = True
        else:
            context['reverse'] = False
        return context


class WordCreateView(LoginRequiredMixin, CreateView):
    model = Word
    form_class = WordCreateForm
    success_url = reverse_lazy('word:create')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        word = form.save(commit=False)
        word.from_lang = self.request.user.profile.learn
        word.to_lang = self.request.user.profile.language
        return super().form_valid(form)


class WordQueryView(LoginRequiredMixin, FormView):
    form_class = WordQueryForm
    template_name = 'word/word_query.html'
    success_url = reverse_lazy('word:query')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = self.request.session.get('query_result', None)
        if not results:
            return context
        context['results'] = [obj.object for obj in serializers.deserialize("json", results)]
        del self.request.session['query_result']
        return context

    def form_valid(self, form):
        query_string = form.cleaned_data['query_string']
        language = form.cleaned_data['language']
        if language == self.request.user.profile.learn.code:
            results = Word.objects.filter(source__icontains=query_string)
        else:
            results = Word.objects.filter(translation__icontains=query_string)
        self.request.session['query_result'] = serializers.serialize("json", results)
        return super().form_valid(form)


class WordUpdateView(LoginRequiredMixin, UpdateView):
    model = Word
    form_class = WordUpdateForm
    success_url = reverse_lazy('home')


@require_GET
def ignore_word(request, pk):
    """
    Ignore a word by excluding it with the user's profile.
    """
    word = Word.objects.get(pk=pk)
    word.excluded_by_user.add(request.user.profile)
    return JsonResponse({'status': 'Word ignored!'})
