from django.forms.models import ModelForm


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
