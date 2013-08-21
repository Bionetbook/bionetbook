from protocols.forms import verbs as verb_forms
from protocols.forms import forms

def get_verb_list():
    verb_list = []
    for attr_name in dir(verb_forms):
        form_candidate = getattr(verb_forms, attr_name, None)
        try:
            if issubclass(form_candidate, forms.Form):
                verb_list.append(form_candidate)
        except TypeError:
            continue
    return verb_list


VERB_LIST = get_verb_list()
VERB_CHOICES = [(x.slug, x.name) for x in VERB_LIST]
VERB_FORM_DICT = {x.slug: x for x in VERB_LIST}

MACHINE_VERBS = [x.slug for x in VERB_LIST if x.has_machine]
COMPONENT_VERBS = [x.slug for x in VERB_LIST if x.has_component]
THERMOCYCLER_VERBS = [x.slug for x in VERB_LIST if x.has_thermocycler]
MANUAL_VERBS = [x.slug for x in VERB_LIST if x.has_manual]
MANUAL_LAYER = dict((x.slug, x.layers) for x in VERB_LIST if x.layers)

# MANUAL_LAYER={'mix':['technique_comment','duration','duration_units'],
#                 'place':['item_to_place','target','conditional_statement','technique_comment','duration','duration_units'],
#                 'discard':['item_to_discard','item_to_retain','conditional_statement','technique_comment','duration','duration_units'],
#                 'let-sit-stand':'settify',
#                 'store':'settify',
#                 'transfer':['item_to_place','old_vessel','new_vessel','item_to_discard','technique_comment','min_vol','vol_units','duration','duration_units'],
#                 'dry':['technique_comment'],
#                 }

def settify(settings_dict, shorthand = True, summary = False, action = False, comments = False):

    settings = []
    units = ''
    output = {}
    
    # Duration replaces min_time if None, or not present. 


    # if 'duration' in settings_dict:
    #     if 'min_time' not in settings_dict or not settings_dict['min_time']:
    #         settings_dict['min_time'] = settings_dict['duration']

    # if 'duration_units' in settings_dict:
    #     if 'time_units' not in settings_dict or not settings_dict['time_units']: 
    #         settings_dict['time_units'] = settings_dict['duration_units']            

    items = ['temp', 'time', 'speed', 'cycle', 'comment', 'conc', 'vol', 'mass', 'link', 'technique']

    for item in items:
        data = dict((k, v) for k, v in settings_dict.iteritems() if item in k and v != None)
        if not data:
            continue
        if item == 'cycle':
            units = None
            numbers = None
            out = None
            
            plural = ' cycles'

            if 'cycle_back_to' in data and 'cycles' in data:
                if data['cycles'] == '1':
                    plural = ' cycle'
                
                numbers = str(data['cycles']) 
                units = plural
                cycle_to = data['cycle_back_to'] 

            if 'cycles' in data and 'cycle_back_to' not in data:
                if data['cycles'] == '1':
                    plural = ' cycle'
                
                numbers = str(data['cycles']) 
                units = plural
            if summary:
                output['cycles'] = numbers
                output['cycle_back_to'] = data.get('cycle_back_to', None)
            else:    
                settings.append(out)

        if item == 'link':
            if summary:
                output['link'] = data['protocol_link']        

        if item == 'technique':
            if 'technique_comment' in settings_dict:
                output['technique_comment'] = settings_dict['technique_comment']

                
        else:        
            max_item = 'max_' + item
            min_item = 'min_' + item  
            unit_item = item + '_units'
            comment_item = item + '_comment'
            units = None
            numbers = None
            out = None

            if max_item in data and min_item in data:
                if data[max_item] == data[min_item]:
                    # units_c = conc['max_conc']
                    numbers = str(data[max_item])
                else:
                    # units_c = data[min_item] + '-' + data[max_item]
                    numbers = str(data[min_item]) + '-' + str(data[max_item])
            else:
                if max_item in data:
                     # units_c = conc[max_item]
                    numbers = str(data[max_item])
                if min_item in data:
                     # units_c = conc[min_item]   
                    numbers = str(data[min_item]) 

            if numbers != None:
                
                if unit_item in data:
                    units = str(data[unit_item])
                else:
                    units = ''
                    # return 'no concentration units specified for %s' % units_dict['name']
                out = str(numbers) + ' ' + units
                    
                if comment_item in data:
                    comment = str(data[comment_item])
                else:
                    comment = None

                if shorthand:
                    units = shorten(units)           

                if comment:
                    output[item] = [numbers, units, comment]

                if summary:
                    output[item] = [numbers, units]    
                else:    
                    settings.append(out)
             
    if summary:
        return output
    else:
        return settings        


def shorten(units):

    d ={'nanograms':'ng',
        'micrograms':'ug',    
        'milligrams':'mg',    
        'grams':'g',  
        'kilograms':'kg', 
        'nanoLiter':'ng', 
        'microLiter':'ul',    
        'microliter':'ul',    
        'milliLiter':'ml',    
        'Liters':'L',
        'nanoMolar':'nM', 
        'microMolar':'uM',    
        'milliMolar':'mM',    
        'Molar':'M',
        'nanomole':'nm', 
        'micromole':'um',    
        'millimole':'mm',    
        'mole':'m',
        'nanograms/microLiter': 'ng/ul',
        'Units/microliter': 'U/ul',
        'Units': 'U',
        # 'X':'X',
        'minutes':'min', 
        'minute':'min', 
        'mins':'min', 
        'minu':'min', 
        'seconds':'sec',    
        'second':'sec',    
        'sec':'sec',    
        'hour':'hr',    
        'hours':'hr',    
        'day':'d',  
        'days':'d',  
        'degrees Celsius':'C', 
        'celsius':'C', 
        'farenheit':'F', 
        'kelvin':'K', 
        }

    try:
        short_units = d[units]
    except KeyError:
        short_units = units

    return short_units


def labeler(object_dict):
    output = {}
    
    if object_dict['verb'] in MANUAL_VERBS:
        verb_attrib_order = list(MANUAL_LAYER[object_dict['verb']]) # if this is not deep copied, the pop(settify) messes it up
        output['display_order'] = verb_attrib_order
        
        for item in verb_attrib_order:
            if 'name' in object_dict.keys():
                output['name'] = object_dict['name']
            if item in object_dict.keys():
                output[item] = object_dict[item]
            if 'duration' in object_dict.keys() and 'duration_units' in object_dict.keys():
                output['time'] = [object_dict['duration'], object_dict['duration_units']]    
            if 'duration' in object_dict.keys() and 'duration_units' not in object_dict.keys():
                output['time'] = [object_dict['duration'], 'sec']    
            if 'settify' in item:
                output.update(settify(object_dict, summary=True))    

        if 'settify' in verb_attrib_order:
            
            settify_order = ['temp', 'speed', 'conc', 'vol', 'mass', 'time', 'technique_comment', 'link']
            [output['display_order'].append(r) for r in settify_order if r in output.keys()]
            output['display_order'].pop(output['display_order'].index('settify'))
        
    return output 
        
def get_timeunit(time_var, desired_unit = 'sec'):
    ''' time_var = [value_str, 'units']
    return (float(min_value), [,float(max_value)], 'units', 'original units')
    '''
    factor = {
        'sec' : {'sec': 1, 'min': 60, 'hrs': 3600,'h': 3600, 'd' : 86400, 'yrs':  31536000},
        'min' : {'sec': 1/60, 'min': 1, 'hrs': 60, 'h': 60,'d' : 1440, 'yrs':  525600},
        'hrs' : {'sec': 1/3600, 'min': 1/60, 'hrs': 1, 'h': 1, 'd' : 24, 'yrs':  8760},
        'h' : {'sec': 1/3600, 'min': 1/60, 'hrs': 1, 'h': 1, 'd' : 24, 'yrs':  8760},
        'd' : {'sec': 1/86400, 'min': 1/3600, 'hrs': 1/60, 'h': 1/60, 'd' : 1, 'yrs':  365},
        'yrs' : {'sec': 1/31536000, 'min': 1/525600, 'hrs': 1/8760, 'h': 1/8760, 'd' : 1/365, 'yrs':  1},
        }
    if isinstance(time_var[0], str) and '-' in time_var[0]:    

        min_time = str(time_var[0][:time_var[0].index('-')])
        max_time = str(time_var[0][time_var[0].index('-')+1:])

        return ((float(factor[desired_unit][time_var[1]]) * float(min_time)), 
                (float(factor[desired_unit][time_var[1]]) * float(max_time)), 
                desired_unit, 
                time_var[1])
    else:
        return ((float(factor[desired_unit][time_var[1]]) * float(time_var[0])),
                desired_unit, 
                time_var[1])

def eval_time(_dict, value = 'min_time'):
    ''' time_var = [value_str, 'units']
    return (float(min_value), [,float(max_value)], 'units', 'original units')
    '''

    # action_min_time = 0
    # action_max_time = 0
    time_unit = 'sec'

    factor = {
        'sec' : {'sec': 1, 'min': 60, 'hrs': 3600,'h': 3600, 'd' : 86400, 'yrs':  31536000},
        'min' : {'sec': 1/60, 'min': 1, 'hrs': 60, 'h': 60,'d' : 1440, 'yrs':  525600},
        'hrs' : {'sec': 1/3600, 'min': 1/60, 'hrs': 1, 'h': 1, 'd' : 24, 'yrs':  8760},
        'h' : {'sec': 1/3600, 'min': 1/60, 'hrs': 1, 'h': 1, 'd' : 24, 'yrs':  8760},
        'd' : {'sec': 1/86400, 'min': 1/3600, 'hrs': 1/60, 'h': 1/60, 'd' : 1, 'yrs':  365},
        'yrs' : {'sec': 1/31536000, 'min': 1/525600, 'hrs': 1/8760, 'h': 1/8760, 'd' : 1/365, 'yrs':  1},
        }
    
    if 'time_units' in _dict and _dict['time_units'] is not None:
        time_unit = _dict['time_units']

    if value in _dict and _dict[value] is not None:
        return float(factor['sec'][time_unit]) * float(_dict[value])

    try: 
        return float(factor['sec'][time_unit]) * float(_dict['min_time'])
    except:
        return 0