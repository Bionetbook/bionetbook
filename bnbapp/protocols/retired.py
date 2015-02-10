# retired.py

def objectid2name(self, objid, **kwargs):
    
        ''' function takes in a protocol instance (self) and an objid. If the objid is not in the protocol instance, a False is returned. 
        if the objid is in the protocol it returns a list:
        nodetype = True : step action or reagent
        name = True: returns the name of the object.
        location = True: returns a (step, action) location. If step, it returns a single int.
        
        attributes = True: return list of all attribute names
        units = True: returns a shorthand format for reagent units
        parents = True: returns parents
        
        full_data = True: adds (merges) all key: value pairs from the object to the outDict. object_data overrites 
        not completed:
        siblings = True: returns all siblings
        
        children = True: returns children
        

        ''' 

        default_setting = {}
        default_setting['objectid'] = objid
        default_setting['nodetype'] =  'None'
        default_setting['name'] = 'None'
        default_setting['location'] = []
        default_setting['full_data'] = False
        outDict = {}
        
        # Merging the 2 dicts together, kwargs overites default settings:
        if kwargs:
            for k, v in itertools.chain(default_setting.iteritems(), kwargs.iteritems()):
                outDict[k] = v 
        else:
            for k, v in default_setting.iteritems():
                outDict[k] = v 


        # make lists of all objectid's:
        steps_by_id = [r['objectid'] for r in self.steps]
        #[self.steps[r]['objectid'] for r in range(self.get_num_steps)]
        
        # actions_by_id = self.get_action_tree('objectid')
        actions_by_id = [i[2] for i in self.get_action_tree('objectid')]

        reagents_by_id = [i[0] for i in self.get_reagent_data('objectid')]

        # find what nodetype of objectid:
        if objid in steps_by_id:
            outDict['nodetype'] = 'step'
            outDict['name'] = self.nodes[objid]['name']
            outDict['location'] = [steps_by_id.index(objid)]
            outDict['object_data']  = self.nodes[objid]
            # outDict['slug'] = 
        
        if objid in actions_by_id:
            outDict['nodetype'] = 'action'
            outDict['name'] = self.nodes[objid]['name']
            outDict['location'] = self.get_action_tree()[actions_by_id.index(objid)][:-1]
            outDict['object_data'] = self.nodes[objid]


        if objid in reagents_by_id:
            outDict['nodetype'] = 'reagent'
            outDict['name'] = self.nodes[objid]['name']
            outDict['location'] = self.get_reagent_data('detail')[reagents_by_id.index(objid)][1:3]
            s = self.get_reagents_by_action()
            for k,v in s.items():
                if objid in v:
                    reagent_order = s[k].index(objid)

            outDict['location'].append(reagent_order)
            outDict['object_data'] = self.nodes[objid]
        

        if kwargs:    
        # Return general requensts:   
            if 'attributes' in kwargs and kwargs['attributes'] == True: 
                outDict['attributes'] = outDict['object_data'].keys()
            
            if 'units' in kwargs and kwargs['units'] == True:
                outDict['label'] = unify(outDict['object_data'])

            if 'children' in kwargs and kwargs['children'] == True:
                if outDict['nodetype'] == 'step':
                    outDict['children'] = [r['objectid'] for r in self.nodes[objid]['actions']]
                if outDict['nodetype'] == 'action':
                    outDict['children'] = [r['objectid'] for r in self.nodes[objid][COMPONENT_KEY]]    
                if outDict['nodetype'] == 'reagent':
                     outDict['children'] = None

            if 'parents' in kwargs and kwargs['parents'] == True:
                tmp = self.get_objectid(outDict['location'][0], outDict['location'][1])
                if outDict['nodetype'] =='step':
                    outDict['parents'] = 'protocol'
                if outDict['nodetype'] == 'action':
                    outDict['parents'] = tmp[0]
                if outDict['nodetype'] == 'reagent':
                    outDict['parents'] = tmp[1]        

            if 'full_data' in kwargs and kwargs['full_data']:
                full_data = outDict.pop('object_data')
                temp = {}
                for k, v in itertools.chain(outDict.iteritems(), full_data.iteritems()):
                    temp[k] = v 
                    
                outDict = temp

        # Returm reagent handlers:    
        # destruct object_data unless specicied in options
        if not outDict['full_data'] == True:
            outDict.pop('object_data')
        
        outDict.pop('full_data')    

        return outDict  

def get_reagent_data(self, display=None):
        # function takes the display argument and returns the (step, action) display of the reagent, i.e. verb, objectid, slug etc.  
        ''' this combiones a find technique with a return technique:
        find = self.data['components-location']
        return = through the self.steps accessor and not theough an objid accessor. 


        '''
        self.needed_reagents = []
        
        if self.data['components-location'][0] > 0:  # check if there are components in the protocol:
            for l in self.data['components-location']: # iterate over all step,action locations where there are components
                components_per_cur_list = len(self.steps[l[1]]['actions'][l[2]][COMPONENT_KEY]) 
                for r in range(0,components_per_cur_list):
                    reagent_name = self.steps[l[1]]['actions'][l[2]][COMPONENT_KEY][r]['name']
                    objectid = self.steps[l[1]]['actions'][l[2]][COMPONENT_KEY][r]['objectid']
                    cur_reagent_name = []
                    cur_reagent_name.append(reagent_name)
                    if 'total volume' in reagent_name.lower():
                        continue
                    if display == 'detail':
                        cur_reagent_name.append(l[1])
                        cur_reagent_name.append(l[2])
                    if display == 'all': 
                        tmp = []
                        tmp.append(l[1])
                        tmp.append(l[2])
                        tmp.append(self.steps[l[1]]['actions'][l[2]]['verb'])
                        cur_reagent_name.append(tmp)
                    if display =='name_objectid':
                        cur_reagent_name = (reagent_name, objectid)
                    if display == 'objectid':
                        actionid = self.get_objectid(l[1], l[2])
                        cur_reagent_name = (objectid, actionid[1])
                            
                    self.needed_reagents.append(cur_reagent_name)    

        return self.needed_reagents        


def get_reagents_by_action(self, out_label='objectid'):
        ''' this combiones a find technique with a return technique:
        find = self.data['components-location']
        return = through the self.steps accessor and not theough an objid accessor. 


        '''
        self.verb_reagents = {}
        for l in self.data['components-location']: # iterate over all step,action locations where there are components 
            components_per_cur_list = len(self.steps[l[1]]['actions'][l[2]][COMPONENT_KEY]) # iterate over reagents
            verb = self.steps[l[1]]['actions'][l[2]]['verb']
            verbid = self.steps[l[1]]['actions'][l[2]]['objectid']
            if out_label == 'literal':
                self.verb_reagents[verbid]=[]
            if out_label == 'objectid':
                self.verb_reagents[verbid]=[]

            for r in range(0,components_per_cur_list):
                    reagent_name = self.steps[l[1]]['actions'][l[2]][COMPONENT_KEY][r]['name']
                    if 'total volume' in reagent_name.lower():
                        continue

                    objectid = self.steps[l[1]]['actions'][l[2]][COMPONENT_KEY][r]['objectid']
                    if out_label == 'literal':
                        self.verb_reagents[verbid].append(reagent_name)
                    if out_label == 'objectid':
                        self.verb_reagents[verbid].append(objectid)
        
        return self.verb_reagents          

def get_objectid(self, stepnum, actionnum):
        step = self.steps[stepnum]['objectid']
        action = self.steps[stepnum]['actions'][actionnum]['objectid']
        return (step,action)        