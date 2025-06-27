from django_random_queryset import RandomManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return str(self.name)

    name = models.CharField(_("Language"), max_length=100)
    code = models.CharField(_("Language code"), max_length=5)


class Word(models.Model):

    class Meta:
        verbose_name = _('Word')
        verbose_name_plural = _('Words')
        ordering = ['source']

    def __str__(self):
        return str(self.source)

    objects = RandomManager()

    source = models.CharField(max_length=200, verbose_name=_('Word'))
    translation = models.CharField(max_length=200, verbose_name=_('Translation'))
    from_lang = models.ForeignKey(Language, on_delete=models.CASCADE,related_name='from_lang')
    to_lang = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='+')
