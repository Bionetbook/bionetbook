def settify(settings_dict, shorthand = True):

    settings = []

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
