from django import template

register = template.Library()


@register.simple_tag()
def get_item(index, list):
    return list[index]
