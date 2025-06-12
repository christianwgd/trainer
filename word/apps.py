from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'word'
    verbose_name = _('Word')
