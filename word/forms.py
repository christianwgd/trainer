from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _

from word.models import Word


class WordCreateForm(ModelForm):

    class Meta:
        model = Word
        fields = [
            'source', 'translation',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['source'].label = user.profile.learn
        self.fields['source'].widget.attrs.update({'autofocus': 'autofocus'})
        self.fields['translation'].label = user.profile.language

    def clean_source(self):
        source = self.cleaned_data.get("source")
        if Word.objects.filter(source=source).exists():
            raise ValidationError(
                _('This word already exists.'),
            )
        return source


class WordUpdateForm(ModelForm):

    class Meta:
        model = Word
        fields = [
            'source', 'translation',
        ]


class WordQueryForm(forms.Form):

    query_string = forms.CharField(
        label=_('Query String'),
        max_length=100,
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),
    )
    language = forms.ChoiceField(
        label='Language',
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['language'].choices = [
            (user.profile.language.code, user.profile.language.name),
            (user.profile.learn.code, user.profile.learn.name),
        ]
