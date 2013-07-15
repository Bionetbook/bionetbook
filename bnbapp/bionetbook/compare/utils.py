from protocols.utils import MANUAL_LAYER
# from core.utils import TIME_UNITS

LAYERS = {
        'schedule': 
            ['physical_commitment', 'duration', 'duration_units', 'time_comment',],
        'experiment': 
            ['tube_label', 'tracking_object', ],
        'for_deletion': 
            ['remarks', 'comment_why', 'add_to_what', 'other_settings'],
        'short_term':
            ['output_to_track', 'why', 'vessel_type', 'input_notes', 'describe_where', 
            'output_notes', 'slug', 'input_to_track', 'technique_comment', 'temp_units', 'min_temp', 
            'max_temp', 'speed_units', 'max_speed', 'min_speed', 'model', 'temp_comment',],
        'children_keys': 
            ['speed','tube_label', 'tracking_object', 'duration', 'duration_units', 'time_comment', 
            'comment_why', 'add_to_what', 'other_settings', 'output_to_track', 'why', 'vessel_type', 
            'input_notes', 'describe_where', 'output_notes', 'slug', 'input_to_track','technique_comment',
            'model', 'temp_comment',
            ]
        }


OUTPUT_MASKS = {
                    'manual': ['duration', 'time'],
                }




class ColNum(object):
    def __init__(self,colnum):
        self.colnum = colnum
    def __call__(self, x):
        return x[self.colnum]

def isint(x): 
    if type(x) is int:
        return True
    else:
        return False   


def align_verbs(x, y):
    '''
    method to align names between 2 lists. to add more protocols to the comaprison, chnage the union command to be recursive
     
    '''
    
    r = list(set(x).union(set(y)))
    order = []
    out = []
    for i in r:
        if i in x and i in y:
            order.append((i, x.index(i), y.index(i), x.index(i) + y.index(i)))
        if i in x and i not in y: 
            order.append((i, x.index(i), x.index(i) + 0.5, 2*x.index(i) + 0.5 ))
        if i in y and i not in x: 
            order.append((i, y.index(i) + 0.5, y.index(i), 2*y.index(i) + 0.5)) 

    order.sort(key=ColNum(3))
    
    for row in order:
        if isint(row[1]) and isint(row[2]):
            out.append((row[0], row[0]))
        if isint(row[1]) and not isint(row[2]):
            out.append((row[0], None))  
        if isint(row[2]) and not isint(row[1]):
            out.append((None, row[0]))  
    
    return out


def html_label_two_protocols(x,y,changed, unchanged, current_layer=None, **kwargs):
    stack = []
    if 'machine' in current_layer:
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
    
    if 'components' in current_layer: 
        ''' assuming that the objectids of the reagents are the same'''

        # count how many changes each reagent has, if 2 reagent names are different, write them last 
        _vol = ''
        _conc = ''
        _mass = ''

        # embed link for components that are protocol links:
        
        if 'name' in changed:
            _name = '''
            <TR><TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666">%s</font></TD>''' % (
            str(x['name']), str(y['name'])) 

        if 'name' in unchanged:    
            _name = '<TR><TD color="#C0C0C0" colspan="2">%s</TD>' % x['name']
        
        if 'link' in x.keys():
            _name = '<TR><TD href="%s">%s</TD>' %(x['link'],x['name'])

        # print _name    

        if 'vol' in changed:# and 'vol' not in unchanged:
            _vol = '''
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666">%s</font></TD>'''%(
            str(x['vol'][0]) + str(x['vol'][1]), 
            str(y['vol'][0]) + str(y['vol'][1])) 

        if 'vol' in unchanged:# and 'vol' not in changed:
            _vol = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['vol'][0]) + str(x['vol'][1]))  

        if 'vol' not in changed and 'vol' not in unchanged:
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

        if 'conc' not in changed and 'conc' not in unchanged:
            _conc = '''
            <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
            str('input') )           

        if 'mass' in changed:  #and 'mass' not in unchanged
            _mass = '''
            <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
            <TD color="#015666"><font color="#015666">%s</font></TD>'''%(
            str(x['mass'][0]) + str(x['mass'][1]), 
            str(y['mass'][0]) + str(y['mass'][1])) 
        
        if 'mass' in unchanged: # and 'mass' not in unchanged:
            _mass = '''
            <TD color="#C0C0C0" colspan="2">%s</TD>'''%(
            str(x['mass'][0]) + str(x['mass'][1]))

        if 'mass' not in changed and 'mass' not in unchanged:
            _mass = '''
            <TD color="#C0C0C0" colspan="2"><i>%s</i></TD>'''%(
            str('input') )  

        return  _name + _vol + _conc + _mass + '</TR>'

    if 'thermocycle' in current_layer: 
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
    
    if 'manual' in current_layer:
        _temp = ''
        _time = ''
        _speed = ''
        _name = '<TR>'
        display=[]
        display.append(_name)

        display_order = MANUAL_LAYER[x['verb']] 
        if display_order !='settify':
            for item in display_order:
                tmp= ''
                if item in changed:
                    tmp = '''
                    <TD color="#B82F3"><font color="#B82F3">%s</font></TD>
                    <TD color="#015666"><font color="#015666"> %s</font></TD>'''%(
                    str(x[item]), str(y[item]))

                if item in unchanged and item not in changed:
                    tmp = '''
                    <TD color="#C0C0C0" colspan="2">%s</TD>'''%str(x[item])

                display.append(tmp)         

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

        display.append(_temp)      
    
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

        display.append(_time)    

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

        display.append(_speed)
        display.append('</TR>')

        # return  _name + _temp + _time + _speed + '</TR>' 
        return ''.join(display)

def merge_table_pieces(content_tmp, layers = None):
    ''' label is an HTML object and for automation sake, created by concatenating a few peices:
        table = '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5">' --> defines the table properties in HTML
        content = '<TR><TD>{0}</TD><TD>{1}</TD></TR><TR><TD colspan="2">{2}</TD></TR>' --> generates the content of the comparison table
        merge = '<' + table + content + '</TABLE>>' --> merges the pieces into one line of text. '''
    import itertools
    
    table = '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="1">'
    content = ''.join(list(itertools.chain(*content_tmp)))

    if layers:
        switch = {'components': '<TR><TD colspan="2">Name</TD><TD colspan="2">Volume</TD><TD colspan="2">Conc</TD><TD colspan="2">Mass</TD></TR>',
              'thermocycle': '<TR><TD>Phase name</TD><TD colspan="2">temp</TD><TD colspan="2">time</TD><TD colspan="2">cycles</TD><TD colspan="2">cycle to</TD></TR>'}
        header = switch[layers]          
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











