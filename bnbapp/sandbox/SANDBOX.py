class DiffObject(dict):
    def __init__(self, protocol_a=None, protocol_b=None, objectid_a=None, objectid_b=None, **kwargs):
        #self.parent = parent
        # super(DiffObject, self).__init__(protocol, parent=parent, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

    child_nodes = ['machine', 'components', 'thermocycle']
    
    if objectid_a:
        self.objectid = objectid_a
        self.name = protocol_a.nodes[self.objectid]['name']
        self.child_type = protocol_a.nodes[self.objectid].childtype()
    else:     
        self.objectid = objectid_b
        self.name = protocol_b.nodes[self.objectid]['name']
        self.child_type = protocol_b.nodes[self.objectid].childtype()
    
    
    self.diff_objectid = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
    self.node_type = 'verb'


    if self.child_type in child_nodes:
        if dirty:
            nodes = protocol.nodes[objid].children
            node_dict['child'] = [r.summary for r in protocol.nodes[objid].children]
        else:    
            node_dict['child'] = self.get_child_diff(objid)




class childObject(dict):
    def __init__(self, protocol_a, protocol_b, objectid, **kwargs):

        self.name = [protocol_a.nodes[objectid]['name'], protocol_b.nodes[object_b]['name'] ]  


    def get_item(self, objectid, item):
        try:
            call = self.protocol_A.nodes[objectid]
        except KeyError:
            call = []

        if item in call.keys()
            temp = call['item']
        else:
            temp = getattr(call, item)


                  