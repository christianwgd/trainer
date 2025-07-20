from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _


from word.models import Word


class WordForm(ModelForm):

    class Meta:
        model = Word
        fields = [
            'source', 'translation'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['source'].label = user.profile.learn
        self.fields['translation'].label = user.profile.language

    def clean_source(self):
        source = self.cleaned_data.get("source")
        if Word.objects.filter(source=source).exists():
            raise ValidationError(
                _('This word already exists.'),
            )
        return source
