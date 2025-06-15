from django.forms.models import ModelForm


from userprofile.models import UserProfile


class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'language', 'learn'
        ]
        widgets = {
        }
