from django import template

register = template.Library()


@register.simple_tag()
def get_item(index, word_list):
    return word_list[index]
