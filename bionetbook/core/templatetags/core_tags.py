from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='bootstrapcheck')
def bootstrapcheck(value):
    if value:
        text = '<span class="badge badge-success"><i class="icon-ok icon-white"></i></span>'
    else:
        text = '<span class="badge badge-important"><i class="icon-ok icon-white"></i></span>'
    return mark_safe(text)
