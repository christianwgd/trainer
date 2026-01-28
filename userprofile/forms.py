from django.forms.models import ModelForm
from django_select2.forms import Select2MultipleWidget

from userprofile.models import UserProfile


class BootstrapSelect2MultipleWidget(Select2MultipleWidget):
    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs.setdefault('data-theme', 'bootstrap5')
        return attrs


class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'list_amount', 'pair_amount',
            'exclude',
            'language', 'learn',
        ]
        widgets = {
            'exclude': BootstrapSelect2MultipleWidget,
        }
