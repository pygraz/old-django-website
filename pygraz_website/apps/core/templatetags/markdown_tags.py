import markdown2

from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.filter(name='markdown')
def markdown(value):
    """
    Basic markdown filter used throughout the site.
    """
    return mark_safe(markdown2.markdown(value, safe_mode=True))
