# def rebuild_steps(self):
# self.steps_data = [ Step(protocol=self, data=s) for s in self.data['steps'] ]

class NodeBase(dict):
    """Base class for the protocol components"""

    keylist = ['name','objectid']
    badkeys = {'component - list': 'components', 'reagent_name': 'name'}

    # ADD _meta CLASS TO USE SOME EXTRA DB-LIKE FUNCTIONALITY

    class Meta:
        def __init__(self, component):
            self.component = component

        def get_all_field_names(self):
            result = self.component.keys()
            result.sort()
            return result

    def __init__(self, protocol, data={}, **kwargs):
        super(NodeBase, self).__init__(**kwargs)
        print 'node initiates of %s' %data['objectid']
        print 'node %s has keys %s'%(data['objectid'], data.keys())
        self.protocol = protocol

        self['objectid'] = None #self.get_hash_id()
        self['slug'] = None

        self._meta = NodeBase.Meta(self)

        # if set(badkeys.keys())

        for fm in self.keylist:       # REQUIRED ATTRIBUTES
            self[item] = None
        print 'sending %s to update' %data['objectid']
        self.update_data(data)
        print 'finished updating %s'%data['objectid']
        print 'node %s has keys %s'%(data['objectid'], data.keys())    

    @property
    def slug(self):
        if not self['slug']:
            self['slug'] = slugify(self['objectid'])
        return self['slug']

    def update_data(self, data={}, **kwargs):
        for key in data:
            self[key] = data[key]

        if not 'name' in self or not self['name']:
            self['name'] = self['slug']    

        #for item in kwargs:             # OVERRIDE DATA WITH ANY PARTICULAR KWARGS PASSED
        #    self[item] = kwargs[item]

    def __unicode__(self):
        return self['slug']

    def rename_attributes(self, BADKEYS):

        def switch(target, this, tothat):
            target[tothat] = target[this]
            del(target[this]) 


for step in b:
    if 'actions' in step.keys():
        for action in step['actions']:
            for k,v in BADKEYS.iteritems():
                if k in action:
                    switch(action,k,v)

                    # if 'component - list' in action:    
                        # action['components'] = action['component - list']
                        # del(action['component - list'])            
                        # for component in action['components']:
                        #     if 'reagent_name' in component:
                        #         component['name'] = component['reagent_name']
                        #         del(component['reagent_name']) 
    
    @property
    def title(self):
        return self.protocol.name

    @property
    def parent(self):
        return self.protocol    

class Step(NodeBase):

    def update_data(self, data={}, **kwargs):
        print 'Step super update data %s' % data['objectid']
        super(Step, self).update_data(data=data, **kwargs) # Method may need to be changed to handle giving it a new name.
        print 'Step return super update data %s' % data['objectid']
        if 'actions' in data:
            print 'Step send action creation %s' % data['objectid']
            self['actions'] = [ Action(self.protocol, step=self, data=a) for a in data['actions'] ]
            print 'Step return action creation %s' % data['objectid']
        else:
            self['actions'] = []

        # UPDATE DURATION AT THE SAME TIME
        duration = 0
        for action in self['actions']:
            if 'duration' in action:
                duration += int(action['duration'])

        self['duration'] = duration

    def get_absolute_url(self):
        return reverse("step_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self['slug'] })

    @property
    def title(self):
        return "%s - %s" % (self.protocol.name, self['name'])

class Action(NodeBase):

    def __init__(self, protocol, step=None, data=None, **kwargs):
        print 'Action initializing, income Step is  %s'% step['objectid']
        self.step = step
        print 'Action send super action init with  %s' % data['objectid']
        super(Action, self).__init__(protocol, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.
        print 'Action super for init on step %s' % data['objectid']
    def update_data(self, data={}, **kwargs):
        super(Action, self).update_data(data=data, **kwargs) # Method may need to be changed to handle giving it a new name.
        # print 'super action update data with %s' % data['objectid']
        print 'node %s has keys %s'%(data['objectid'], self.keys())
        print 'replacing keys'    
        if 'component - list' in data:
            data['components'] = data['component - list']
            del(data['component - list'])
            print 'node %s has keys %s'%(data['objectid'], self.keys())    
            print 'action call component with %s' % data['objectid']
            self['component - list'] = [ Component(self.protocol, action=self, data=c) for c in data['component - list'] ]
            print 'action return component with %s' % data['objectid']
        else:
            self['component - list'] = []

    #def set_name(self):
    #    self['name'] = self['verb']

    def get_absolute_url(self):
        return reverse("action_detail", kwargs={'protocol_slug': self.step.protocol.slug, 'step_slug':self.step.slug, 'action_slug':self.slug })

    @property
    def title(self):
        return "%s - %s - %s" % (self.protocol.name, self.step['name'], self['name'])
    
    @property
    def parent(self):
        return self.step
class Component(NodeBase):
    def __init__(self, protocol, action=None, data=None, **kwargs):
        self.action = action
        print 'initiated component %s with income action %s' % (data['objectid'], action['objectid'])
        print 'Super component init with %s' % data['objectid']
        super(Component, self).__init__(protocol, data=data, **kwargs) # deleted action = self   Method may need to be changed to handle giving it a new name.
    
    def update_data(self, data={}, **kwargs):
        print 'component updating data'
        print 'super component update data'
        super(Component, self).update_data(data=data, **kwargs) # Method may need to be changed to handle giving it a new name.
        # print 'updated action %s' % data['objectid']

        self.parent_node = self.action['objectid']# print 'initiated super of component %s' %data['objectid']

    def get_absolute_url(self):
        return reverse("component_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self.action.step.slug, 'action_slug':self.action.slug, 'component_slug':self.slug  })

    @property
    def title(self):
        return "%s - %s - %s" % (self.protocol.name, self.action.step['name'], self.action['name'], self['name'])        

    @property
    def parent(self):
        return self.action


