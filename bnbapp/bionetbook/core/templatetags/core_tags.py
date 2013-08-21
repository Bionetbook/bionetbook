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


@register.filter(name='breadcrumb')
def breadcrumb(value):
    '''
    Expects an ordered list of dictionaries 
    example: [{'url':"/", 'name':"bob"},{}]
    '''
    result = []
    for item in value:
        if not 'url' in item:
            result.append( '<li class="active">%(name)s</li>' % item )
        else:
            result.append( '<li><a href="%(url)s">%(name)s</a><span class="divider">/</span></li>' % item )

    return "\n".join(result)


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
    
    if not value:
        return None
    max_time = 0    

    time = value.split('-')
    min_time = format_time(float(time[0]))
    if len(time) > 1: 
        max_time = format_time(float(time[1]))
    
    if max_time > 0: 
        if min_time == max_time:
            return str(min_time)
        else: 
            return str(min_time)+ "-" + str(max_time)    
    else: 
        return str(min_time)

@register.filter(name='protocol_time_compact')
def protocol_time_compact(value):
    if not value:
        return None 
    max_time = 0

    # max_time = None    
    time = value.split('-')
    min_time = format_time(float(time[0]), compact=True)
    if len(time)>1:
        max_time = format_time(float(time[1]), compact=True)

    if max_time > 0:     
        if min_time == max_time:
            return str(min_time)
        else: 
            return str(min_time)+ "-" + str(max_time)   

    else: 
        return str(min_time)        

    

@register.filter(name='protocol_time_round_up')
def protocol_time_round_up(value):
    if not value:
        return None 
    max_time = 0

    # max_time = None    
    time = value.split('-')
    min_time = format_time(float(time[0]), rounding=True)
    if len(time)>1:
        max_time = format_time(float(time[1]), rounding=True)

    if max_time > 0:     
        if min_time == max_time:
            return str(min_time)
        else: 
            return str(min_time)+ "-" + str(max_time)   

    else: 
        return str(min_time)        

def format_time(value, rounding = False, compact = False):

    h=0
    m,s = divmod(value, 60)

    if m> 60:
        h,m = divmod(m, 60)
        if h > 24:
            d,h = divmod(h, 24)
            if compact:
                return "%dd:%02dh:%02dm" % (d, h, m)                
            if rounding:
                return "%dd:%02dh:%02dm" % (d, h, m+1)            
            else:
                return "%dd:%02dh:%02dm:%02ds" % (d, h, m, s)        
        else:
            if compact:
                return "%dh:%02dm" % (h, m)        
            if rounding:
                return "%dh:%02dm" % (h, m+1)        
            else:
                return "%dh:%02dm:%02ds" % (h, m, s)            
    else:
        if compact:       
            return "%02dm" % (m) 
        if rounding:       
            return "%02dm" % (m+1)
        else:
            return "%dh:%02dm:%02ds" % (h, m, s)


    # if unicode(value)[-1] == 's':
    #     return "%s'" % value
    # else:
    #     return "%s's" % value
