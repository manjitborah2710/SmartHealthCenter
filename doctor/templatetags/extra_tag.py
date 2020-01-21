from django import template

register = template.Library()

@register.filter(name = 'inGroup')
def inGroup(user, group_name):
    return user.groups.filter(name=group_name).exists() or user.is_superuser

