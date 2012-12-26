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


@register.inclusion_tag('core/model_instance_data_table.html')
def object_data_table(model_instance):
    # NEEDS TO BE UPDATED TO HANDLE DICTIONARIES

    fields = []
    raw = None

    for field_name in model_instance._meta.get_all_field_names():
        if field_name not in ['data', 'actions']:  # USED TO NOT DISPLAY RAW DOCUMENT DATA
            try:
                value = model_instance[field_name]
            except:
                try:
                    value = getattr(model_instance, field_name, None)
                except:
                    value = None

            if field_name == "raw":
                raw = dict(
                    key=field_name,
                    value=mark_safe(value)

                )
                continue
            field = dict(
                key=field_name,
                value=value
            )
            fields.append(field)
    fields.append(raw)
    return {'fields': fields}
