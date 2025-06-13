from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from word.models import Word


class WordListView(LoginRequiredMixin, ListView):
    model = Word

    def get_queryset(self):
        return Word.objects.order_by('?')
