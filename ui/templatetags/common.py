from django import template

register = template.Library()

@register.filter
def split_dot_first(str):
    return str.split('.')[0]

@register.filter
def split_path_last(str):
    return str.split('/')[-1]
