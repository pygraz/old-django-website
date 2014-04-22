from django.template import Library
from django.utils.safestring import mark_safe
from markdown import Markdown

register = Library()


@register.filter(name='markdown')
def markdown(value):
    """
    Basic markdown filter used throughout the site.
    """
    md = Markdown(safe_mode='escape')
    return mark_safe(md.convert(value))
