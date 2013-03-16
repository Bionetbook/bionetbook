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

# print [x.name for x in VERB_LIST]
def shorten(units, reverse = False):

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
        'X':'X',
        'minutes':'m', 
        'minute':'m', 
        'mins':'m', 
        'minu':'m', 
        'seconds':'s',    
        'second':'s',    
        'sec':'s',    
        'hour':'hr',    
        'hours':'hr',    
        'day':'d',  
        'days':'d',  
        'celsius':'C', 
        'farenheit':'F', 
        'kelvin':'K', 
        }

    if reverse:
        pass
    else:
        try:
            short_units = d[units]
        except KeyError:
            short_units = units

        return short_units

def settify(settings_dict, shorthand = True, summary = False):

    settings = []
    units = ''
    output = {}

    temp = dict((k, v) for k, v in settings_dict.iteritems() if 'temp' in k and v != None)
    time = dict((k, v) for k, v in settings_dict.iteritems() if 'time' in k and v != None)
    speed = dict((k, v) for k, v in settings_dict.iteritems() if 'speed' in k and v != None)
    cycle = dict((k, v) for k, v in settings_dict.iteritems() if 'cycle' in k and v != None)
    comment = dict((k, v) for k, v in settings_dict.iteritems() if 'comment' in k or 'why' in k and v != None )
    

    if temp: 
        units = None
        numbers = None
        out = None

        if 'temp_units' in temp:
            units = str(temp['temp_units'])
        # else: 
        #     units = 'Celsius'

        if 'max_temp' in temp and 'min_temp' in temp:
            
            if temp['min_temp'] == temp['max_temp']:
                numbers =  temp['max_temp']
            else:
                numbers =  temp['min_temp'] + '-' + temp['max_temp']        
        else:
            if 'max_temp' in temp:
                 numbers = temp['max_temp']

            if 'min_temp' in temp:
                 numbers = temp['min_temp']  

        out = str(numbers) + ' ' + units
            
        if 'temp_comment' in temp:
                out = str(out) + ', ' + 'Remark: ' + temp['temp_comment']    

        if shorthand:
            units = shorten(units)
        
        if summary:
            output['temp'] = [numbers, units]

        else:    
            settings.append(out)


    if time: 
        units = None
        numbers = None
        out = None
        
        if 'time_units' in time:
            units = str(time['time_units'])
        # else: 
        #     units = 'Celsius'

        if 'max_time' in time and 'min_time' in time:
            
            if time['min_time'] == time['max_time']:
                numbers =  time['max_time']
            else:
                numbers =  time['min_time'] + '-' + time['max_time']        
        else:
            if 'max_time' in time:
                 numbers = time['max_time']

            if 'min_time' in time:
                 numbers = time['min_time']  

        out = str(numbers) + ' ' + units
            
        if 'time_comment' in time:
                out = str(out) + ', ' + 'Remark: ' + time['time_comment']    

        if shorthand:
            units = shorten(units)        
        
        if summary:
            output['time'] = [numbers, units]

        else:    
            settings.append(out) 

    if speed: 
        units = None
        numbers = None
        out = None
        
        if 'speed_units' in speed:
            units = str(speed['speed_units'])
        else: 
            units = 'RPM'

        if 'max_speed' in speed and 'min_speed' in speed:
            
            if speed['min_speed'] == speed['max_speed']:
                numbers =  speed['max_speed']
            else:
                numbers =  speed['min_speed'] + '-' + speed['max_speed']        
        else:
            if 'max_speed' in speed:
                 numbers = speed['max_speed']

            if 'min_speed' in speed:
                 numbers = speed['min_speed']  

        out = str(numbers) + ' ' + units
            
        if 'speed_comment' in speed:
                out = str(out) + ', ' + 'Remark: ' + speed['speed_comment']    

        if shorthand:
            units = shorten(units)        
                
        if summary:
            output['speed'] = [numbers, units]

        else:    
            settings.append(out)    

    if cycle:
        units = None
        numbers = None
        out = None
        
        plural = ' cycles'

        if 'cycle_to' in cycle and 'cycles' in cycle:
            if cycle['cycles'] == '1':
                plural = ' cycle'
            
            numbers = str(cycle['cycles']) 
            units = plural
            cycle_to = cycle['cycle_to'] 

        if 'cycles' in cycle and 'cycle_to' not in cycle:
            if cycle['cycles'] == '1':
                plural = ' cycle'
            
            numbers = str(cycle['cycles']) 
            units = plural

        if summary:
            output['cycle'] = [numbers, cycle.get('cycle_to', '')]

        else:    
            settings.append(out)    



    # if shorthand == True and out != None:
    #     for out in settings:

    #         out = out.replace('minutes','min') 
    #         out = out.replace('seconds','sec')    
    #         out = out.replace('hour','hr')    
    #         out = out.replace('day','d')  
    #         out = out.replace('celsius','C') 
    #         out = out.replace('farenheit','F') 
    #         out = out.replace('kelvin','K')  
       
    if summary:
        return output
    else:
        return settings


def unify(units_dict, shorthand = True, summary = False):

    units_c = ''
    units_v = ''
    units_m = ''
    output = {}
    

    conc = dict((k, v) for k, v in units_dict.iteritems() if 'conc' in k)
    vol = dict((k, v) for k, v in units_dict.iteritems() if 'vol' in k)
    mass = dict((k, v) for k, v in units_dict.iteritems() if 'mass' in k)

    if conc:
        # check that all data is present:
        if not conc['conc_units']:
            return 'no concentration units specified for %s' % units_dict['name']
        if shorthand:
            conc_units = shorten(conc['conc_units'])      
        if 'max_conc' not in conc and 'min_conc' not in conc:
            return 'enter concentration units for %s' % units_dict['name']    

        if 'max_conc' in conc and 'min_conc' in conc:
            if conc['max_conc'] == conc['min_conc']:
                units_c = conc['max_conc']
            else:
                units_c = conc['min_conc'] + '-' + conc['max_conc']
        
        else:
            if 'max_conc' in conc:
                 units_c = conc['max_conc']
            if 'min_conc' in conc:
                 units_c = conc['min_conc']   

        if summary:
            output['conc'] = [units_c, conc_units]
        else:    
            units_c = units_c + ' ' + conc_units 
        

    
    if vol:
        if not vol['vol_units']:
            return 'no Volume units specified for %s' % units_dict['name']
        if shorthand:
            vol_units = shorten(vol['vol_units'])  


        if 'max_vol' not in vol and 'min_vol' not in vol:
            return 'enter Volume units for %s' % units_dict['name']

        if 'max_vol' in vol and 'min_vol' in vol:

            if vol['max_vol'] == vol['min_vol']:
                
                units_v = vol['max_vol']
            else:
                units_v = vol['min_vol'] + '-' + vol['max_vol']
        else:
            if 'max_vol' in vol:
                 units_v = vol['max_vol']
            if 'min_vol' in vol:
                 units_v = vol['min_vol']          
        
        if summary:
            output['vol'] = [units_v, vol_units]            
        else:
            units_v = units_v + ' ' + vol_units
        

    if mass:
        if not mass['mass_units']:
            return 'no mass units specified for %s' % units_dict['name']
        if shorthand:
            mass_units = shorten(mass['mass_units'])

        if 'max_mass' not in mass and 'min_mass' not in mass:
            return 'enter mass units for %s' % units_dict['name']

        if 'max_mass' in mass and 'min_mass' in mass:

            if mass['min_mass'] == mass['max_mass']:
                units_m = mass['max_mass']
            else:
                units_m = mass['min_mass'] + '-' + mass['max_mass']

        else:
            if 'max_mass' in mass:
                 units_m = mass['max_mass']
            if 'min_mass' in mass:
                 units_m = mass['min_mass']

        if summary:
            output['mass'] = [units_m, mass_units]
        else:    
            units_m = units_m + ' ' + mass_units

    if summary:
        return output
    else:
        return units_c + units_v + units_m