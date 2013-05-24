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


def get_verb_index(x, y):
    r = list(set(x).union(set(y)))
    out = []
    for (cnt, i) in enumerate(r):
        if i in x and i in y:
            out.append((i, x.index(i), y.index(i)), x.index(i) + y.index(i))
        if i in x and i not in y: 
            out.append((i, x.index(i), x.index(i) + 0.5, x.index(i) + y.index(i)))
        if i in y and i not in x: 
            out.append((i, y.index(i) + 0.5, y.index(i), x.index(i) + y.index(i))) 

    return out                  





class tree(object):






