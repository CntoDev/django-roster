from django import template

register = template.Library()


def value_of(value, arg):
    func = getattr(value, arg)
    return func()


register.filter('value_of', value_of)