from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from word.forms import WordForm
from word.models import Word


class WordListView(LoginRequiredMixin, ListView):
    model = Word

    def get_queryset(self):
        amount = 20  # TODO: Make this configurable in user settings
        return Word.objects.order_by('?')[:amount]

    def get_template_names(self):
        if self.request.path.endswith('reverse/'):
            return ['word/word_reverse.html']
        return ['word/word_list.html']


class WordCreateView(LoginRequiredMixin, CreateView):
    model = Word
    form_class = WordForm
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


class WordUpdateView(LoginRequiredMixin, UpdateView):
    model = Word
    form_class = WordForm
    success_url = reverse_lazy('home')
