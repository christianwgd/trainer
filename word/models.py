from django.db import models
from django.utils.translation import gettext_lazy as _
from django_random_queryset import RandomManager


class Language(models.Model):

    name = models.CharField(_("Language"), max_length=100)
    code = models.CharField(_("Language code"), max_length=5)

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return str(self.name)


class Word(models.Model):

    source = models.CharField(max_length=200, verbose_name=_('Word'))
    translation = models.CharField(max_length=200, verbose_name=_('Translation'))
    from_lang = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='from_lang')
    to_lang = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='+')
    created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, related_name='created',
        null=True, blank=True,
    )
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, related_name='modified',
        null=True, blank=True,
    )

    objects = RandomManager()

    class Meta:
        verbose_name = _('Word')
        verbose_name_plural = _('Words')
        ordering = ['source']

    def __str__(self):
        return str(self.source)
