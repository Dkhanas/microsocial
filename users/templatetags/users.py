from django import template
from microsocial import settings

register = template.Library()

@register.filter
def get_avatar(user):
    try:
        return user.avatar.url
    except ValueError:
        return '{}microsocial/images/default/default_avatar.png'.format(settings.STATIC_URL)