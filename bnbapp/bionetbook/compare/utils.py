def html_label_two_protocols(x,y,changed, unchanged, **kwargs):

    stack = []
    if 'machine' in kwargs:
        _temp = ''
        _time = ''
        _speed = ''

        _name = '<TR><TD>%s</TD>' %x['name']        

        if 'temp' in changed:
            _temp = '''
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666"> %s</font></TD>'''%(
            str(x['temp'][0]) + str(x['temp'][1]), 
            str(y['temp'][0]) + str(y['temp'][1]))
        
        if 'temp' in unchanged and 'temp' not in changed:
            _temp = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['temp'][0]) + ' ' + str(x['temp'][1]))   

        # else:
        #     _temp = '''
        #     <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
        #     str('input') )            
    
        if 'time' in changed:
            _time = '''
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666"> %s</font></TD>'''%(
            str(x['time'][0]) + ' ' + str(x['time'][1]), 
            str(y['time'][0]) + ' ' + str(y['time'][1]))
        
        if 'time' in unchanged and 'time' not in changed:
            _time = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['time'][0]) + ' ' + str(x['time'][1]))

        # else:
        #     _time = '''
        #     <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
        #     str('input') )     
    
        if 'speed' in changed:
            _speed = '''
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666"> %s</font></TD>'''%(
            str(x['speed'][0]) + str(x['speed'][1]), 
            str(y['speed'][0]) + str(y['speed'][1]))
        
        if 'speed' in unchanged and 'speed' not in changed:
            _speed = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['speed'][0]) + ' ' + str(x['speed'][1]))

        # else:
        #     _speed = '''
        #     <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
        #     str('input') )     

        return  _name + _temp + _time + _speed + '</TR>'
    
    if 'components' in kwargs: 
        ''' assuming that the objectids of the reagents are the same'''

        # count how many changes each reagent has, if 2 reagent names are different, write them last 
        _vol = ''
        _conc = ''
        _mass = ''

        # embed link for components that are protocol links:
        _name = '<TR><TD>%s</TD>' % x['name']
        if 'link' in x.keys():
            _name = '<TR><TD href="%s">%s</TD>' %(x['link'],x['name'])

        if 'vol' in changed and 'vol' not in unchanged:
            _vol = '''
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666">%s</font></TD>'''%(
            str(x['vol'][0]) + str(x['vol'][1]), 
            str(y['vol'][0]) + str(y['vol'][1])) 

        if 'vol' in unchanged and 'vol' not in changed:
            _vol = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['vol'][0]) + str(x['vol'][1]))  

        else:
            _vol = '''
            <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
            str('input') ) 
 
        if 'conc' in changed:
            _conc = '''
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666">%s</font></TD>'''%(
            str(x['conc'][0]) + str(x['conc'][1]), 
            str(y['conc'][0]) + str(y['conc'][1]))  
            
        if 'conc' in unchanged and 'conc' not in changed:
            _conc = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['conc'][0]) + str(x['conc'][1]))     

        else:
            _conc = '''
            <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
            str('input') ) 
                  

        if 'mass' in changed and 'mass' not in unchaged:
            _mass = '''
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666">%s</font></TD>'''%(
            str(x['mass'][0]) + str(x['mass'][1]), 
            str(y['mass'][0]) + str(y['mass'][1])) 
        
        if 'mass' in unchanged and 'mass' not in unchanged:
            _mass = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['mass'][0]) + str(x['mass'][1]))

        else:
            _mass = '''
            <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
            str('input') )     

        return  _name + _vol + _conc + _mass + '</TR>'

    if 'thermocycle' in kwargs: 
        ''' assuming that the objectids of the reagents are the same'''

        _temp = ''
        _time = ''
        _cycle = ''

        _name = '<TR><TD>%s</TD>' % x['name'].replace('_',' ')

        if 'temp' in changed:
            _temp = ''' 
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666">%s</font></TD>'''%(
            str(x['temp'][0]) + str(x['temp'][1]), 
            str(y['temp'][0]) + str(y['temp'][1]))
            
        if 'temp' in unchanged and 'temp' not in changed:
            _temp = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['temp'][0]) + str(x['temp'][1]))

        else:
            _temp = '''
            <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
            str('input') )         

        if 'time' in changed and 'time' not in unchanged:
            _time = '''
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666">%s</font></TD>'''%(
            str(x['time'][0]) + str(x['time'][1]), 
            str(y['time'][0]) + str(y['time'][1]))

        if 'time' in unchanged and 'time' not in changed:
            _time = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['time'][0]) + str(x['time'][1]))

        else:
            _time = '''
            <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
            str('input') )     

        if 'cycle' in changed and 'cycle' not in unchanged:
            if x['cycle'][1] == y['cycle'][1]:
                _cycle = '''
                <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
                <TD color="#015666"><font color="#015666">%s</font></TD>
                <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
                str(x['cycle'][0]), 
                str(y['cycle'][0]), 
                str(x['cycle'][1]))
            
            if x['cycle'][0] == y['cycle'][0]:
                _cycle = '''
                <TD color="#C0C0C0"><font color="#C0C0C0">%s</font></TD>
                <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
                <TD color="#015666" colspan="2">%s</TD>'''%(
                str(x['cycle'][0]), 
                str(x['cycle'][1]), 
                str(y['cycle'][1])) 

            else:
                _cycle = '''
                <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
                <TD color="#015666"><font color="#015666">%s</font></TD>
                <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
                <TD color="#015666"><font color="#015666">%s</font></TD>'''%(
                str(x['cycle'][0]), 
                str(y['cycle'][0]), 
                str(x['cycle'][1]),
                str(y['cycle'][1])) 
        
        if 'cycle' in unchanged and 'cycle' not in changed:
            _cycle = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
                str(x['cycle'][0]),
                str(x['cycle'][1])) 

        
        return  _name + _temp + _time + _cycle + '</TR>'
    
    if 'manual' in kwargs:
        _temp = ''
        _time = ''
        _speed = ''

        _name = '<TR>'     

        if 'temp' in changed:
            _temp = '''
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666"> %s</font></TD>'''%(
            str(x['temp'][0]) + str(x['temp'][1]), 
            str(y['temp'][0]) + str(y['temp'][1]))
        
        if 'temp' in unchanged and 'temp' not in changed:
            _temp = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['temp'][0]) + ' ' + str(x['temp'][1]))    

        # else:
        #     _temp = '''
        #     <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
        #     str('input') )               
    
        if 'time' in changed:
            _time = '''
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666"> %s</font></TD>'''%(
            str(x['time'][0]) + ' ' + str(x['time'][1]), 
            str(y['time'][0]) + ' ' + str(y['time'][1]))
        
        if 'time' in unchanged and 'time' not in changed:
            _time = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['time'][0]) + ' ' + str(x['time'][1]))

        # else:
        #     _time = '''
        #     <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
        #     str('input') )         
    
        if 'speed' in changed:
            _speed = '''
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666"> %s</font></TD>'''%(
            str(x['speed'][0]) + str(x['speed'][1]), 
            str(y['speed'][0]) + str(y['speed'][1]))
        
        if 'speed' in unchanged and 'speed' not in changed:
            _speed = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['speed'][0]) + ' ' + str(x['speed'][1]))

        # else:
        #     _speed = '''
        #     <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
        #     str('input') )         

        return  _name + _temp + _time + _speed + '</TR>' 

def merge_table_pieces(content_tmp, layer = None):
    ''' label is an HTML object and for automation sake, created by concatenating a few peices:
        table = '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5">' --> defines the table properties in HTML
        content = '<TR><TD>{0}</TD><TD>{1}</TD></TR><TR><TD colspan="2">{2}</TD></TR>' --> generates the content of the comparison table
        merge = '<' + table + content + '</TABLE>>' --> merges the pieces into one line of text. '''
    import itertools
    
    table = '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="1">'
    content = ''.join(list(itertools.chain(*content_tmp)))

    if layer:
        switch = {'components': '<TR><TD>Name</TD><TD colspan="2">Volume</TD><TD colspan="2">Conc</TD><TD colspan="2">Mass</TD></TR>',
              'thermocycle': '<TR><TD>Phase name</TD><TD colspan="2">temp</TD><TD colspan="2">time</TD><TD colspan="2">cycles</TD><TD colspan="2">cycle to</TD></TR>'}
        header = switch[layer]          
        merge = '<' + table + header + content + '</TABLE>>'

    else:
        merge = '<' + table + content + '</TABLE>>'
    return merge


def add_step_label(step_text, step_layer = False): 
    import textwrap
    wrapped = textwrap.wrap(step_text, 60)
    stack = []
    for w in wrapped:
        stack.append('<font>%s</font><br/>'%w)
    
    merge = '<' + ''.join(stack) +'>'   
    return merge











