from django.template import Context, Template
from django.test import TestCase


class MarkdownFilterTests(TestCase):
    def test_html_escaping(self):
        """
        The markdown template filter should remove HTML in its default
        configuration.
        """
        expected = "<p>&lt;i&gt;Some HTML&lt;/i&gt;</p>"
        tmpl = Template("{% load markdown_tags %}{{ data|markdown }}")
        result = tmpl.render(Context({"data": "<i>Some HTML</i>"}))
        self.assertEqual(expected, result)
