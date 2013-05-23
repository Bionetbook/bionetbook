SANDBOX
def action_children(self):
    out = []
    for action in self.get_actions:
        children = self.nodes[action].children
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

make list
cycle through step ids
create step dictionary:
    step_dict = {}
    stepdict[step] = []
    for action in step:
        actiondict = {}
        actiondict[action] = []
        for node in action:
            nodedict = {}
            nodedict[node] = []

        stepdict[step].append(actiondict) 


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


def protocol_tree_json(self):
    out = []
    for step in self.get_steps:
        step_dict={}
        step_dict[step] = []
        actions = [r['objectid'] for r in self.nodes[step].children] 
        for action in actions:
            action_dict = {}
            children = self.nodes[action].children
            if children:
                if type(children) is list:
                    action_dict[action] = [r['objectid'] for r in self.nodes[action].children]
                else: 
                     action_dict[action] = children['objectid']       
            else: 
                action_dict[action] = None

            step_dict[step].append(action_dict)    
            
        out.append(step_dict)






class tree(object):






