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

def settify(settings_dict, shorthand = True, summary = False):

    settings = []
    units = ''
    output = {}
    items = ['temp', 'time','speed','cycle','comment', 'conc','vol','mass']

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
                # else:
                #     units = ''
                    # return 'no concentration units specified for %s' % units_dict['name']
                out = str(numbers) + ' ' + units
                    
                if comment_item in data:
                    out = 'Remark: ' + data[comment_item]  

                if shorthand:
                    units = shorten(units)           

                if summary:
                    output[item] = [numbers, units]
                else:    
                    settings.append(out)
             
    if summary:
        return output
    else:
        return settings        


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
        # 'X':'X',
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
        'degrees Celsius':'C', 
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



# def unify(settings_dict, shorthand = True, summary = False):

    # temp = dict((k, v) for k, v in settings_dict.iteritems() if 'temp' in k and v != None)
    # time = dict((k, v) for k, v in settings_dict.iteritems() if 'time' in k and v != None)
    # speed = dict((k, v) for k, v in settings_dict.iteritems() if 'speed' in k and v != None)
    # cycle = dict((k, v) for k, v in settings_dict.iteritems() if 'cycle' in k and v != None)
    # comment = dict((k, v) for k, v in settings_dict.iteritems() if 'comment' in k or 'why' in k and v != None )
    # conc = dict((k, v) for k, v in settings_dict.iteritems() if 'conc' in k and v != None)
    # vol = dict((k, v) for k, v in settings_dict.iteritems() if 'vol' in k and v != None)
    # mass = dict((k, v) for k, v in settings_dict.iteritems() if 'mass' in k and v != None)


    # if conc:
    #     units = None
    #     numbers = None
    #     out = None

    #     if 'max_conc' in conc and 'min_conc' in conc:
    #         if conc['max_conc'] == conc['min_conc']:
    #             # units_c = conc['max_conc']
    #             numbers = conc['max_conc']
    #         else:
    #             units_c = conc['min_conc'] + '-' + conc['max_conc']
    #             numbers = conc['min_conc'] + '-' + conc['max_conc']
    #     else:
    #         if 'max_conc' in conc:
    #              # units_c = conc['max_conc']
    #             numbers = conc['max_conc']
    #         if 'min_conc' in conc:
    #              # units_c = conc['min_conc']   
    #             numbers = conc['min_conc'] 

    #     if numbers != None:
            
    #         if 'conc_units' in conc:
    #             units = str(conc['conc_units'])
    #         # else:
    #         #     units = ''
    #             # return 'no concentration units specified for %s' % units_dict['name']
    #         out = str(numbers) + ' ' + units
                
    #         if 'conc_comment' in conc:
    #             out = 'Remark: ' + conc['conc_comment']  

    #         if shorthand:
    #             units = shorten(units)           

    #         if summary:
    #             output['conc'] = [numbers, units]
    #         else:    
    #             settings.append(out)
    
    # if vol:  
    #     units = None
    #     numbers = None
    #     out = None  
        
    #     if 'max_vol' in vol and 'min_vol' in vol:
    #         if vol['max_vol'] == vol['min_vol']:
    #             units_c = vol['max_vol']
    #             numbers = vol['max_vol']
    #         else:
    #             units_c = vol['min_vol'] + '-' + vol['max_vol']
    #             numbers = vol['min_vol'] + '-' + vol['max_vol']
    #     else:
    #         if 'max_vol' in vol:
    #              units_c = vol['max_vol']
    #              numbers = vol['max_vol']
    #         if 'min_vol' in vol:
    #              units_c = vol['min_vol']   
    #              numbers = vol['min_vol'] 

    #     if numbers != None:
            
    #         if 'vol_units' in vol:
    #             units = str(vol['vol_units'])
    #         # else:
    #         #     units = ''
    #             # return 'no volentration units specified for %s' % units_dict['name']
    #         out = str(numbers) + ' ' + units
                
    #         if 'vol_comment' in vol:
    #             out = 'Remark: ' + vol['vol_comment']  

    #         if shorthand:
    #             units = shorten(units)           

    #         if summary:
    #             output['vol'] = [numbers, units]
    #         else:    
    #             settings.append(out)
        

    # if mass:
    #     if 'max_mass' in mass and 'min_mass' in mass:
    #         if mass['max_mass'] == mass['min_mass']:
    #             units_c = mass['max_mass']
    #             numbers = mass['max_mass']
    #         else:
    #             units_c = mass['min_mass'] + '-' + mass['max_mass']
    #             numbers = mass['min_mass'] + '-' + mass['max_mass']
    #     else:
    #         if 'max_mass' in mass:
    #              units_c = mass['max_mass']
    #              numbers = mass['max_mass']
    #         if 'min_mass' in mass:
    #              units_c = mass['min_mass']   
    #              numbers = mass['min_mass'] 

    #     if numbers != None:
            
    #         if 'mass_units' in mass:
    #             units = str(mass['mass_units'])
    #         # else:
    #         #     units = ''
    #             # return 'no massentration units specified for %s' % units_dict['name']
    #         out = str(numbers) + ' ' + units
                
    #         if 'mass_comment' in mass:
    #             out = 'Remark: ' + mass['mass_comment']  

    #         if shorthand:
    #             units = shorten(units)           

    #         if summary:
    #             output['mass'] = [numbers, units]
    #         else:    
    #             settings.append(out)


    # if temp:
    #     if 'max_temp' in temp and 'min_temp' in temp:
            
    #         if temp['min_temp'] == temp['max_temp']:
    #             numbers =  temp['max_temp']
    #         else:
    #             numbers =  temp['min_temp'] + '-' + temp['max_temp']        
    #     else:
    #         if 'max_temp' in temp:
    #              numbers = temp['max_temp']

    #         if 'min_temp' in temp:
    #              numbers = temp['min_temp']  

    #     if numbers != None:
            
    #         if 'temp_units' in temp:
    #             units = str(temp['temp_units'])
            
    #         out = str(numbers) + ' ' + units    

    #         if 'temp_comment' in temp:
    #                 out = str(out) + ', ' + 'Remark: ' + temp['temp_comment']    

    #         if shorthand:
    #             units = shorten(units)
            
    #         if summary:
    #             output['temp'] = [numbers, units]

    #         else:    
    #             settings.append(out)


    # if time: 
    #     units = None
    #     numbers = None
    #     out = None
        
    #     if 'max_time' in time and 'min_time' in time:
            
    #         if time['min_time'] == time['max_time']:
    #             numbers =  time['max_time']
    #         else:
    #             numbers =  time['min_time'] + '-' + time['max_time']        
    #     else:
    #         if 'max_time' in time:
    #              numbers = time['max_time']

    #         if 'min_time' in time:
    #              numbers = time['min_time']  

    #     if nummbers != None:

            
    #         if 'time_units' in time:
    #             units = str(time['time_units'])            
            
    #         out = str(numbers) + ' ' + units

    #         if 'time_comment' in time:
    #                 out = str(out) + ', ' + 'Remark: ' + time['time_comment']    

    #         if shorthand:
    #             units = shorten(units)        
            
    #         if summary:
    #             output['time'] = [numbers, units]

    #         else:    
    #             settings.append(out) 

    # if speed: 
    #     units = None
    #     numbers = None
    #     out = None
        
        

    #     if 'max_speed' in speed and 'min_speed' in speed:
            
    #         if speed['min_speed'] == speed['max_speed']:
    #             numbers =  speed['max_speed']
    #         else:
    #             numbers =  speed['min_speed'] + '-' + speed['max_speed']        
    #     else:
    #         if 'max_speed' in speed:
    #             numbers = speed['max_speed']

    #         if 'min_speed' in speed:
    #              numbers = speed['min_speed']  

    #     if numbers != None:
            
    #         if 'speed_units' in speed:
    #             units = str(speed['speed_units'])
    #         else: 
    #             units = 'RPM'        
    #         out = str(numbers) + ' ' + units
            
    #         if 'speed_comment' in speed:
    #             out = str(out) + ', ' + 'Remark: ' + speed['speed_comment']    

    #         if shorthand:
    #             units = shorten(units)        
                    
    #         if summary:
    #             output['speed'] = [numbers, units]

    #         else:    
    #             settings.append(out)    

    # if cycle:
    #     units = None
    #     numbers = None
    #     out = None
        
    #     plural = ' cycles'

    #     if 'cycle_to' in cycle and 'cycles' in cycle:
    #         if cycle['cycles'] == '1':
    #             plural = ' cycle'
            
    #         numbers = str(cycle['cycles']) 
    #         units = plural
    #         cycle_to = cycle['cycle_to'] 

    #     if 'cycles' in cycle and 'cycle_to' not in cycle:
    #         if cycle['cycles'] == '1':
    #             plural = ' cycle'
            
    #         numbers = str(cycle['cycles']) 
    #         units = plural

    #     if summary:
    #         output['cycle'] = [numbers, cycle.get('cycle_to', '')]

    #     else:    
    #         settings.append(out)    
   
    # if summary:
    #     return output
    # else:
    #     return settings


