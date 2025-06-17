from django.forms.models import ModelForm


from word.models import Word


class WordForm(ModelForm):

    class Meta:
        model = Word
        fields = [
            'source', 'translation'
        ]

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            user = kwargs.pop('user')
        else:
            user = None
        super().__init__(*args, **kwargs)
        if user:
            self.fields['source'].label = user.profile.learn
            self.fields['translation'].label = user.profile.language
