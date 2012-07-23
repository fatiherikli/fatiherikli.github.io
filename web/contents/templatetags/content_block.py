from django import template

from contents.models import ContentBlock


register = template.Library()

@register.simple_tag
def content_block(name):
    try:
        contentblock = ContentBlock.objects.get(name=name)
    except ContentBlock.DoesNotExist:
        return ""
    return contentblock.content.rendered

register.simple_tag(content_block)