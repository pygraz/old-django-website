import html

from django.template import Library
from django.utils.safestring import mark_safe
from markdown import Markdown

register = Library()


@register.filter(name="markdown")
def markdown(value):
    """
    Basic markdown filter used throughout the site.
    """
    md = Markdown()
    markdown_html = md.convert(html.escape(value))
    return mark_safe(markdown_html)
