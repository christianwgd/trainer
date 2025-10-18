from django.db import models
from django.contrib import auth
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from word.models import Language, Word


User = auth.get_user_model()
lang = getattr(settings, "LANGUAGE_CODE", 'de')


class UserProfile(models.Model):

    class Meta:
        verbose_name = _("User setting")
        verbose_name_plural = _("User settings")

    def __str__(self):
        return str(self.ref_usr)

    ref_usr = models.OneToOneField(
        User, on_delete=models.CASCADE,
        verbose_name=_("User"), related_name='profile',
    )
    language = models.ForeignKey(
        Language, on_delete=models.PROTECT, related_name='profiles',
        verbose_name=_('Language'), null=True, blank=True
    )
    learn = models.ForeignKey(
        Language, on_delete=models.PROTECT, related_name='learners',
        verbose_name=_('Learning Language'), null=True
    )
    exclude = models.ManyToManyField(
        Word, related_name='excluded_by_user',
        verbose_name=_('Excluded Words'), blank=True
    )
    list_amount = models.PositiveIntegerField(
        default=20, verbose_name=_('List Amount'),
        help_text=_('Amount of words to show in the list')
    )
    pair_amount = models.PositiveIntegerField(
        default=10, verbose_name=_('Pair Amount'),
        help_text=_('Amount of word pairs to show')
    )


@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    """
        Function to create user profile.
        sender is the model class that sends the signal,
        while instance is an actual instance of that class
    """

    user = instance
    profile, _created = UserProfile.objects.get_or_create(ref_usr=user)
    if _created:
        profile.language = Language.objects.filter(code=lang).first()
        profile.save()
