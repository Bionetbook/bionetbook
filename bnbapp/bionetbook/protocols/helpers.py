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
            'minutes':'min', 
            'seconds':'sec',    
            'hour':'hr',    
            'day':'d',  
            'celsius':'C', 
            'farenheit':'F', 
            'kelvin':'K', 
            }

        if reverse:
            pass
        else:
            return d[units]

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
            units = str(units) + ' ' + str(temp['temp_units'])
            
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


def unify(units_dict, shorthand = True, summary = False):

    units_c = ''
    units_v = ''
    units_m = ''
    output = {}
    # print summary

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
                units_c = units_c + conc['min_conc'] + '-' + conc['max_conc']
        else:
            if 'max_conc' in conc:
                 units_c = conc['max_conc']
            if 'min_conc' in conc:
                 units_c = conc['min_conc']   

        # print units_c                              
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
                units_v = units_v + ', ' + vol['max_vol']
            else:
                units_v = units_v + ', ' + vol['min_vol'] + '-' + vol['max_vol']

        else:
            if 'max_vol' in vol:
                 units_v = vol['max_vol']
            if 'min_vol' in vol:
                 units_v = vol['min_vol']          
        
        # print units_v
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
                units_m = units_m + ', ' + mass['max_mass']
            else:
                units_m = units_m + ', ' + mass['min_mass'] + '-' + mass['max_mass']

        else:
            if 'max_mass' in mass:
                 units_m = mass['max_mass']
            if 'min_mass' in mass:
                 units_m = mass['min_mass']

        # print units_m         
        if summary:
            output['mass'] = [units_m, mass_units]
        else:    
            units_m = units_m + ' ' + mass_units

        

    




        # units_m = units_m.replace('nanograms','ng') 
        # units_m = units_m.replace('micrograms','ug')    
        # units_m = units_m.replace('milligrams','mg')    
        # units_m = units_m.replace('grams','g')  
        # units_m = units_m.replace('kilograms','kg') 
        # units_v = units_v.replace('nanoLiter','ng') 
        # units_v = units_v.replace('microLiter','ul')    
        # units_v = units_v.replace('microliter','ul')    
        # units_v = units_v.replace('milliLiter','ml')    
        # units_v = units_v.replace('Liters','L')
        # units_c = units_c.replace('nanoMolar','nM') 
        # units_c = units_c.replace('microMolar','uM')    
        # units_c = units_c.replace('milliMolar','mM')    
        # units_c = units_c.replace('Molar','M')
        # units_c = units_c.replace('nanomole','nm') 
        # units_c = units_c.replace('micromole','um')    
        # units_c = units_c.replace('millimole','mm')    
        # units_c = units_c.replace('mole','m')

    if summary:
        # print '4th update'
        return output
    else:
        return units_c + units_v + units_m