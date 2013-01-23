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

def settify(settings_dict, shorthand = True):

    settings = []
    units = ''

    temp = dict((k, v) for k, v in settings_dict.iteritems() if 'temp' in k)
    time = dict((k, v) for k, v in settings_dict.iteritems() if 'time' in k)
    speed = dict((k, v) for k, v in settings_dict.iteritems() if 'speed' in k)
    comment = dict((k, v) for k, v in settings_dict.iteritems() if 'comment' in k or 'why' in k)

    if temp: 
        
        if 'max_temp' in temp and 'min_temp' in temp:
            
            if temp['min_temp'] == temp['max_temp']:
                units =  temp['max_temp']
            else:
                units =  temp['min_temp'] + '-' + temp['max_temp']        
        else:
            if 'max_temp' in temp:
                 units = temp['max_temp']

            if 'min_temp' in temp:
                 units = temp['min_temp']  
        
        if 'temp_units' in temp:
            units = units + ' ' + temp['temp_units']
            
        if 'temp_comment' in temp:
                units = units + ', ' + 'Remark: ' + temp['temp_comment']    
        
        settings.append(units) 

    if time: 
        
        if 'max_time' in time and 'min_time' in time:
            
            if time['min_time'] == time['max_time']:
                units =  time['max_time']
            else:
                units =  time['min_time'] + '-' + time['max_time']        
        else:
            if 'max_time' in time:
                 units = time['max_time']

            if 'min_time' in time:
                 units = time['min_time']  
        
        if 'time_units' in time:
            units = units + ' ' + time['time_units']
            
        if 'time_comment' in time:
                units = units + ', ' + 'Remark: ' + time['time_comment']    
        
        settings.append(units) 

    if speed: 
        
        if 'max_speed' in speed and 'min_speed' in speed:
            
            if speed['min_speed'] == speed['max_speed']:
                units =  speed['max_speed']
            else:
                units =  speed['min_speed'] + '-' + speed['max_speed']        
        else:
            if 'max_speed' in speed:
                 units = speed['max_speed']

            if 'min_speed' in speed:
                 units = speed['min_speed']  
        
        if 'speed_units' in speed:
            units = units + ' ' + speed['speed_units']
            
        if 'speed_comment' in speed:
                units = units + ', ' + 'Remark: ' + speed['speed_comment']    
        
        settings.append(units)    

    if shorthand == True:
        for units in settings:

            units = units.replace('minutes','min') 
            units = units.replace('seconds','sec')    
            units = units.replace('hour','hr')    
            units = units.replace('day','d')  
            units = units.replace('celsius','C') 
            units = units.replace('farenheit','F') 
            units = units.replace('kelvin','K')  
       
    return settings


def unify(units_dict, shorthand = True):

    units = ''

    conc = dict((k, v) for k, v in units_dict.iteritems() if 'conc' in k)
    vol = dict((k, v) for k, v in units_dict.iteritems() if 'vol' in k)
    mass = dict((k, v) for k, v in units_dict.iteritems() if 'mass' in k)

    if conc:
        # check that all data is present:
        if not conc['conc_units']:
            return 'no concentration units specified for %s' % units_dict['name']
        if 'max_conc' not in conc and 'min_conc' not in conc:
            return 'enter concentration units for %s' % units_dict['name']    

        if 'max_conc' in conc and 'min_conc' in conc:

            if conc['max_conc'] == conc['min_conc']:
                units = conc['max_conc']
            else:
                units = units + conc['min_conc'] + '-' + conc['max_conc']
        else:
            if 'max_conc' in conc:
                 units = conc['max_conc']
            if 'min_conc' in conc:
                 units = conc['min_conc']                        
            
        units = units + ' ' + conc['conc_units']  

    
    if vol:
        if not vol['vol_units']:
            return 'no Volume units specified for %s' % units_dict['name']
        if 'max_vol' not in vol and 'min_vol' not in vol:
            return 'enter Volume units for %s' % units_dict['name']

        if 'max_vol' in vol and 'min_vol' in vol:

            if vol['max_vol'] == vol['min_vol']:
                units = units + ', ' + vol['max_vol']
            else:
                units = units + ', ' + vol['min_vol'] + '-' + vol['max_vol']

        else:
            if 'max_vol' in vol:
                 units = vol['max_vol']
            if 'min_vol' in vol:
                 units = vol['min_vol']          
        
        units = units + ' ' + vol['vol_units'] 

    if mass:
        if not mass['mass_units']:
            return 'no mass units specified for %s' % units_dict['name']
        if 'max_mass' not in mass and 'min_mass' not in mass:
            return 'enter mass units for %s' % units_dict['name']

        if 'max_mass' in mass and 'min_mass' in mass:

            if mass['min_mass'] == mass['max_mass']:
                units = units + ', ' + mass['max_mass']
            else:
                units = units + ', ' + mass['min_mass'] + '-' + mass['max_mass']

        else:
            if 'max_mass' in mass:
                 units = mass['max_mass']
            if 'min_mass' in mass:
                 units = mass['min_mass']

        units = units + ' ' + mass['mass_units']

    if shorthand == True:
        units = units.replace('nanograms','ng') 
        units = units.replace('micrograms','ug')    
        units = units.replace('milligrams','mg')    
        units = units.replace('grams','g')  
        units = units.replace('kilograms','kg') 
        units = units.replace('nanoLiter','ng') 
        units = units.replace('microLiter','ul')    
        units = units.replace('microliter','ul')    
        units = units.replace('milliLiter','ml')    
        units = units.replace('Liters','L')
        units = units.replace('nanoMolar','nM') 
        units = units.replace('microMolar','uM')    
        units = units.replace('milliMolar','mM')    
        units = units.replace('Molar','M')
        units = units.replace('nanomole','nm') 
        units = units.replace('micromole','um')    
        units = units.replace('millimole','mm')    
        units = units.replace('mole','m')

    return units