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
        if field_name not in ['data', 'actions', 'components', 'thermocycle', 'machine', 'actions', 'slug', 'name', 'component - list', 'objectid', 'protocols', 'raw']:  # USED TO NOT DISPLAY RAW DOCUMENT DATA
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


@register.filter(name='possesive')
def possesive(value):
    if unicode(value)[-1] == 's':
        return "%s'" % value
    else:
        return "%s's" % value


@register.filter(name='protocoltree')
def protocoltree(value):
    # GET A LIST OF EACH STEP
        # HREF EACH STEP, EXCEPT IF IT IS THIS ONE

        # GET A LIST OF EACH STEP'S ACTION
        # HREF EACH ACTION, EXCEPT IF IT IS THIS ONE

    #if value:
    #    text = '<span class="badge badge-success"><i class="icon-ok icon-white"></i></span>'
    #else:
    #    text = '<span class="badge badge-important"><i class="icon-ok icon-white"></i></span>'
    return mark_safe("<b>PROTOCOL TREE</b>")


@register.filter(name='protocol_time')
def protocol_time(value):
    # def fit_closest_time_unit(time_var, input_unit = 'sec'):
    max_time = None
    if not value:
        return None

    if '-' in value:
        min_time = float(value[:value.index('-')])
        max_time = float(value[value.index('-')+1:])
    else:
        min_time = float(value)

    
    
    value1 = format_time(min_time)

    if max_time:
        value2 = format_time(max_time)
        return str(value1) + '-' + str(value2)
    else:
        return str(value1)


@register.filter(name='protocol_time_round_up')
def protocol_time_round_up(value):
    # def fit_closest_time_unit(time_var, input_unit = 'sec'):
    max_time = None
    if not value:
        return None    

    if '-' in value:
        min_time = float(value[:value.index('-')])
        max_temp = value[value.index('-')+1:]
        max_time = float(max_temp)
    else:
        min_time = float(value)

    value1 = format_time(min_time, rounding=True)

    if max_time:
        value2 = format_time(max_time, rounding=True)
        if value1 != value2:
            return str(value1) + '-' + str(value2)
        else:     
            return str(value1)
    else:
        return str(value1)



def format_time(value, rounding = False):

    h=0
    m,s = divmod(value, 60)

    if m> 60:
        h,m = divmod(m, 60)
        if h > 24:
            d,h = divmod(h, 24)
            if rounding:
                return "%dd:%02dh:%02dm" % (d, h, m+1)            
            else:
                return "%dd:%02dh:%02dm:%02ds" % (d, h, m, s)        
        else:
            if rounding:
                return "%dh:%02dm" % (h, m+1)        
            else:
                return "%dh:%02dm:%02ds" % (h, m, s)            
    else: 
        if rounding:       
            return "%dh%02dm" % (h, m+1)
        else:
            return "%dh:%02dm:%02ds" % (h, m, s)


    # if unicode(value)[-1] == 's':
    #     return "%s'" % value
    # else:
    #     return "%s's" % value
