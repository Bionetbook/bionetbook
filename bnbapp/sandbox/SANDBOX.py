def get_child_diff(self, parent_id, **kwargs):
        ''' this method is called knowing that the parent_id has children
        '''
        
        out = []
        children_a = self.protocol_A.nodes[parent_id].children # either one or more children
        children_b = self.protocol_B.nodes[parent_id].children

        
        children_A = [r['objectid'] for r in self.protocol_A.nodes[parent_id].children if self.protocol_A.nodes[parent_id].childtype() is not None ]
        children_B = [r['objectid'] for r in self.protocol_B.nodes[parent_id].children if self.protocol_B.nodes[parent_id].childtype() is not None ]
        
        both = list(set(children_A).intersection(set(children_B)))    
        unique_A = list(set(children_A)-set(children_B))
        unique_B = list(set(children_B)-set(children_A)) 
        
        if len(both) == 1:
            temp = self.child_compare(0, both[0])        
            if temp:
                out.append(temp)
            
        if len(both) > 1:
            for (cnt, item) in enumerate(both):    
                temp = self.child_compare(cnt, item) 
                if temp:
                    out.append(temp)

        if len(unique_A) == 1:
            temp = self.child_dict(0, unique_A[0], side = 'LEFT')
            if temp:
                out.append(temp)
            
        if len(unique_A) > 1:
            for (cnt, item) in enumerate(unique_A):    
                temp = self.child_dict(cnt, item, side = 'LEFT') 
                if temp:
                    out.append(temp)

        if len(unique_B) == 1:
            temp = self.child_dict(0, unique_B[0], side = 'RIGHT')
            if temp:
                out.append(temp)
            
        if len(unique_B) > 1:
            for (cnt, item) in enumerate(unique_B):    
                temp = self.child_dict(cnt, item, side = 'RIGHT') 
                if temp:
                    out.append(temp)                                
        return out             
        
    
    def child_compare(self, cnt, item, **kvargs):    
        dirty = False
        child_dict={}
        LEFT = self.protocol_A
        RIGHT = self.protocol_B
        # child_dict['order'] = str(LEFT.nodes[LEFT.nodes[item].parent['objectid']].childtype()) + ' ' + str(cnt)
        
        child_dict['name'] =  [LEFT.nodes[item]['name'], RIGHT.nodes[item]['name']] 
        child_dict['node_type'] =  str(LEFT.nodes[LEFT.nodes[item].parent['objectid']].childtype())
        child_dict['number'] =  child_dict['node_type'] + ' ' + str(cnt)
        child_dict['diff_objectid'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        child_dict['node_objectid'] = LEFT.nodes[item]['objectid']
        D = DictDiffer(LEFT.nodes[item].summary, RIGHT.nodes[item].summary)
        
        for attr in D.changed():  
            if len(D.changed()) > 0:
                dirty = True
                child_dict[attr] = [LEFT.nodes[item].summary[attr],RIGHT.nodes[item].summary[attr]]
    
        for attr in D.uniq_a():
            if len(D.uniq_a()) > 0:    
                dirty = True
                child_dict[attr] = [LEFT.nodes[item].summary[attr],None]

        for attr in D.uniq_b():
            if len(D.uniq_b()) > 0:    
                dirty = True
                child_dict[attr] = [None, RIGHT.nodes[item].summary[attr]]    

        if dirty:
            return child_dict        
        else:
            return {}    

    def child_dict(self, cnt, item, side = None):
        child_dict={}
        if side == 'LEFT':
            protocol = self.protocol_A
        if side == 'RIGHT': 
            protocol = self.protocol_B
            
        child_dict['name'] =  protocol.nodes[item]['name']
        child_dict['node_type'] =  str(protocol.nodes[protocol.nodes[item].parent['objectid']].childtype())
        child_dict['number'] =  child_dict['node_type'] + ' ' + str(cnt)
        child_dict['diff_objectid'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        child_dict['node_objectid'] = protocol.nodes[item]['objectid']
        # if side == 'LEFT':
        for attr in protocol.nodes[item].summary:
            child_dict[attr] = [protocol.nodes[item].summary[attr], None]
        # if side == 'RIGHT':
        #     for attr in self.protocol_B.nodes[item].summary:        
        #         child_dict[attr] = [None, self.protocol_B.nodes[item].summary[attr]]                      

        return child_dict        