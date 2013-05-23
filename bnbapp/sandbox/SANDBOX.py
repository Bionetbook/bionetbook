SANDBOX
out = []
for step in c.get_steps:
step_dict = {}
step_dict[step] = []
    actions = c.nodes[step].children    
    for action in actions:
        children = list(c.nodes[action].children)
        if children:
            if type(children) is list:
                temp = []
                for child in children:
                    temp.append(child['objectid'])
                out.append({action: temp})
            if type(children) is not list:
                out.append({action: children['objectid']})
        else: 
            out.append({action: None})


out =[]
for step in c.get_steps:
    step_dict={}
    step_dict[step] = []
    actions = [r['objectid'] for r in c.nodes[step].children]
    for action in actions:
        action_dict = {}
        action_dict[action] = []
        children = [r['objectid'] for r in c.nodes[step].children]
        if children:
            if type(children) is list:
                temp = []
                for child in children:
                    temp.append(child['objectid'])
                action_dict[action].append({action: temp})
            if type(children) is not list:
                action_dict[action].append({action: children['objectid']})
        else: 
            action_dict[action].append({action: None})

    out.append(step_dict)


def get_diff_attributes(self, **kwargs):
    child_nodes = ['machine', 'components', 'thermocycle']
    attributes = self.find_diff_verbs()
    non_children_attributes = list(set(attributes)-set(child_nodes))

    out = {}
    for attr in non_children_attributes:
        out[attr] = self.protocol_A.nodes[verb_diff[0][attr]]


    return out




class tree(object):






