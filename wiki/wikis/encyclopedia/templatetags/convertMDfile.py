import markdown

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def convert_markdown_file(content):
    return markdown.markdown(content)
