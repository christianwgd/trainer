from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def lang_flag(lang):
    return mark_safe(
        f'<img src="/static/flags/{lang.code}.svg" '
        f'alt="{lang.name}" class="lang-flag">'
    )
