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
# MANUAL_LAYER={'mix':['technique_comment','duration','duration_units'],
#                 'place':['item_to_place','target','conditional_statement','technique_comment','duration','duration_units'],
#                 'discard':['item_to_discard','item_to_retain','conditional_statement','technique_comment','duration','duration_units'],
#                 'let-sit-stand':'settify',
#                 'store':'settify',
#                 'transfer':['item_to_place','old_vessel','new_vessel','item_to_discard','technique_comment','min_vol','vol_units','duration','duration_units'],
#                 'dry':['technique_comment'],
#                 }

MANUAL_LAYER = dict((x.slug, x.layers) for x in VERB_LIST if x.layers)



# print [x.name for x in VERB_LIST]

def settify(settings_dict, shorthand = True, summary = False, action = False):

    settings = []
    units = ''
    output = {}
    
    # Duration replaces min_time if None, or not present. 


    if 'duration' in settings_dict.keys():
        if 'min_time' not in settings_dict.keys() or not settings_dict['min_time']: 
            settings_dict['min_time'] = settings_dict['duration']    

    if 'duration_units' in settings_dict.keys():
        if 'time_units' not in settings_dict.keys() or not settings_dict['time_units']: 
            settings_dict['time_units'] = settings_dict['duration_units']            

    items = ['temp', 'time', 'speed', 'cycle', 'comment', 'conc', 'vol', 'mass', 'link']

    for item in items:
        data = dict((k, v) for k, v in settings_dict.iteritems() if item in k and v != None)
        if not data:
            continue
        if item == 'cycle':
            units = None
            numbers = None
            out = None
            
            plural = ' cycles'

            if 'cycle_to' in data and 'cycles' in data:
                if data['cycles'] == '1':
                    plural = ' cycle'
                
                numbers = str(data['cycles']) 
                units = plural
                cycle_to = data['cycle_to'] 

            if 'cycles' in data and 'cycle_to' not in data:
                if data['cycles'] == '1':
                    plural = ' cycle'
                
                numbers = str(data['cycles']) 
                units = plural
            if summary:
                output[item] = [numbers, data.get('cycle_to', '')]
            else:    
                settings.append(out)

        if item == 'link':
            if summary:
                output['link'] = data['protocol_link']        


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

                if summary:
                    output[item] = [numbers, units, comment]
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
        display_order = MANUAL_LAYER[object_dict['verb']]
        
        if len(display_order) == 1 and display_order[0] == 'settify':
            output = settify(object_dict, summary=True)
        else:
            for item in display_order:
                if item in object_dict.keys():
                    output[item] = object_dict[item]
        
        output['verb'] = object_dict['verb']

    return output 
        












