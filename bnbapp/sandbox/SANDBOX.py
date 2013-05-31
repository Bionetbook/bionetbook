SANDBOX
out = []
for step in c.get_steps:
step_dict = {}
step_dict[step] = []
    actions = c.nodes[step].children    
    for action in actions:
        children = list(c.nodes[action].children)
        if children:
            temp = []
            for child in children:
                temp.append(child['objectid'])
            out.append({action: temp})
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
            temp = []
            for child in children:
                temp.append(child['objectid'])
            action_dict[action].append({action: temp})
        else: 
            action_dict[action].append({action: None})

    out.append(step_dict)

_______________________________
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


    r = list(set(x).union(set(y)))
    order = []
    out = []
    for (cnt, i) in enumerate(r):
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




class tree(object):






