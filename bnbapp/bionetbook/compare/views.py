from django.http import HttpResponse
from compare.models import ProtocolPlot, DictDiffer
from django.views.generic import TemplateView, View
from compare.utils import html_label_two_protocols, add_html_cell, merge_table_pieces, add_thermo, set_title_label 




class SingleBaseView(TemplateView):
    template_name = "compare/single_base_default.html"

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''
        context = self.get_context_data()

        context['protocol'] = ProtocolPlot.objects.get(slug=kwargs['protocol_slug'])
        # context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])

        if 'layers' in kwargs:
            context['layer'] = kwargs['layers']

        print 'returning CompareBaseView'
        return self.render_to_response(context)

class SingleBaseGraphicView(View):
    '''
    Returns a graphic representaion of a single protocol in SVG or PNG format.
    '''

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''

        protocol = ProtocolPlot.objects.get(slug=kwargs['protocol_slug'])
        format = "svg"

        # grapher = Grapher(protocol_a, protocol_b, format)
        base = protocol.plot()
        layers = protocol.add_layer(layers = kwargs['layers'])
        # print kwargs['layers']
        img = protocol.agraph.draw(prog='dot', format=format)    

        if format in ['svg']:
            format = format + "+xml"

        response = HttpResponse(img, mimetype='image/%s' % format)
        print 'returning SingleBaseGraphicView'
        return response        


class CompareBaseView(TemplateView):
    template_name = "compare/compare_default.html"

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''
        context = self.get_context_data()

        context['protocol_a'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])

        if 'layers' in kwargs:
            context['layer'] = kwargs['layers']

        print 'returning CompareBaseView'
        return self.render_to_response(context)


class CompareLayersView(CompareBaseView):
    template_name = "compare/compare_layer.html"


class CompareBaseGraphicView(View):
    '''
    Returns a graphic representaion of a comparison in either a SVG or PNG format.
    '''

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''

        protocol_a = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        protocol_b = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
        format = kwargs['format']

        grapher = Grapher(protocol_a, protocol_b, format)
        base = grapher.draw_two_protocols()
        img = base.agraph.draw(prog='dot', format=format)    

        if format in ['svg']:
            format = format + "+xml"

        response = HttpResponse(img, mimetype='image/%s' % format)
        print 'returning CompareBaseGraphicView'
        return response


class CompareLayersGraphicView(View):
    #template_name = "compare/comapare_layer.html"
    '''
        Adds a compare layer to Returns a graphic representaion of a comparison in either a SVG or PNG format.
    '''
    
    def get(self, request, *args, **kwargs):
        '''Gets the context data'''

        protocol_a = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        protocol_b = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
        layers = kwargs['layers']
        format = "svg"

        grapher = Grapher(protocol_a, protocol_b, "svg")
        base = grapher.draw_two_protocols()
        layer = base.add_diff_layer(layers = layers)
        img = layer.agraph.draw(prog='dot', format="svg")    

        if format in ['svg']:
            format = format + "+xml"

        response = HttpResponse(img, mimetype='image/%s' % format)
        print 'returning ComparelayersGraphicView'
        return response


class Grapher(object):
    def __init__(self, protocol_a, protocol_b, format="svg", **kwargs):
        import pygraphviz as pgv

        self.agraph = pgv.AGraph()
        self.protocol_A = protocol_a
        self.protocol_B = protocol_b
        self.agraph.graph_attr['clusterrank'] = 'local'
        self.A_pk = [self.protocol_A.nodes[r].pk for r in self.protocol_A.get_actions] # list of actions in pk-objectid format
        self.B_pk = [self.protocol_B.nodes[r].pk for r in self.protocol_B.get_actions]
        self.matching_verbs_pk = zip(self.A_pk,self.B_pk)
        self.matching_verbs = zip(self.protocol_A.get_actions, self.protocol_B.get_actions)
        self.format = format

    def draw(self):

        # set some default node attributes
        self.agraph.node_attr['style']='filled'
        self.agraph.node_attr['shape']='circle'
        # Define base graph

        # Add edges (and nodes)
        self.agraph.add_edge(1,2)
        self.agraph.add_edge(2,3)
        self.agraph.add_edge(1,3)
        self.agraph.layout() 



        return self.agraph.draw(format=self.format) # draw png


    def draw_two_protocols(self, **kwargs):
        ''' this function draws out 2 base protocols as a sequence of actions. 
            add_layers adds the specified layers that a user wants to compare'''

        # Draw out the first protocol:
            
        for i in range(1, len(self.A_pk)):
            
            self.agraph.add_edge(self.A_pk[i-1], self.A_pk[i])
            e = self.agraph.get_edge(self.A_pk[i-1], self.A_pk[i])
            e.attr['style'] = 'setlinewidth(9)' 
            e.attr['color'] = '#B82F3' 
            n=self.agraph.get_node(self.A_pk[i])
            n.attr['shape']='box'
            n.attr['fontsize'] = '10'
            n.attr['style'] = 'rounded'
            n.attr['label']= self.protocol_A.nodes[self.protocol_A.get_actions[i]]['verb'] #+ '_' + self.protocol_A.nodes[self.protocol_A.get_actions[i]].pk

        # Set the 0'th node and title in protocol_A 
        n = self.agraph.get_node(self.matching_verbs_pk[0][0])
        n.attr['shape']='box'
        n.attr['fontsize'] = '10'
        n.attr['style'] = 'rounded'
        n.attr['label']=self.protocol_A.nodes[self.protocol_A.get_actions[0]]['verb'] #+ '_' + self.protocol_A.nodes[self.protocol_A.get_actions[0]].pk
        # print 'Rendered protocol %s'% self.protocol_A.name
        
        # add base of second protocol:
        for i in range(1, len(self.B_pk)):
            self.agraph.add_edge(self.B_pk[i-1], self.B_pk[i])
            # print 'drawing protocol %s'% self.protocol_B.name
            e = self.agraph.get_edge(self.B_pk[i-1], self.B_pk[i])
            e.attr['style'] = 'setlinewidth(9)' 
            e.attr['color'] = '#015666' 
            n=self.agraph.get_node(self.B_pk[i])
            n.attr['shape']='box'
            n.attr['fontsize'] = '10'
            n.attr['style'] = 'rounded'
            n.attr['label']= self.protocol_B.nodes[self.protocol_B.get_actions[i]]['verb'] #+ '_' + self.protocol_B.nodes[self.protocol_B.get_actions[i]].pk

        # Set the 0'th node in  protocol_A  
        n = self.agraph.get_node(self.matching_verbs_pk[0][1])
        n.attr['shape']='box'
        n.attr['fontsize'] = '10'
        n.attr['style'] = 'rounded'
        n.attr['label']=self.protocol_B.nodes[self.protocol_B.get_actions[0]]['verb'] #+ '_' + self.protocol_B.nodes[self.protocol_B.get_actions[0]].pk

        return self

    def add_diff_layer(self, **kwargs): # , machines = True, components = True, thermocycle = True
        print kwargs['layers']
        if 'machine' in kwargs['layers']:
            machines = True
        else:
            machines = False 
        
        if 'component' in kwargs['layers']:
            components = True
        else:
            components = False 
        
        if 'thermo' in kwargs['layers']:
            thermocycle = True
        else:
            thermocycle = False     

        if 'steps' in kwargs['layers']:
            steps = True
        else:
            steps = False         


        ''' this function assumes that the pairs of objects are equivalent in that both have validated:
            'machines'
            'components'
            'thermocycle'
            'steps' - displays verbatim text. 
            '''
        for verb_a,verb_b in self.matching_verbs: #[(node_a, node_b), ]
            # print verb_a, verb_b
            if 'machine' in self.protocol_A.nodes[verb_a].keys():  # object has only one child:
                # Generate the diff content:
                x = self.protocol_A.nodes[verb_a]['machine'].summary
                y = self.protocol_B.nodes[verb_b]['machine'].summary
                d = DictDiffer (x, y)
                content = html_label_two_protocols(x,y,d.changed(name = True, objectid = True, slug = True), d.unchanged(), machine = True) 

    
                # --->  create a compare-graph-object that will apear between the 2 base diagrams:
                if machines:
                    print 'adding machine layer'
                    diff_object = self.protocol_A.nodes[verb_a]['machine'].pk
                    ea = self.agraph.add_edge(self.protocol_A.nodes[verb_a].pk,diff_object)
                    eb = self.agraph.add_edge(self.protocol_B.nodes[verb_b].pk,diff_object)

                # set all diff objects on same rank:
                    N = self.agraph.add_subgraph([self.protocol_A.nodes[verb_a].pk, diff_object, self.protocol_B.nodes[verb_b].pk], rank = 'same', name = self.protocol_A.nodes[verb_a].pk)#, rankdir='LR') #, name='%s'%(layer_names[nc])) 
                
                # set layout and colors
                    s = self.agraph.get_node(diff_object)
                    s.attr['shape'] = 'box'
                    s.attr['color'] = '#C0C0C0'
                    s.attr['style'] = 'rounded'
                    s.attr['fontsize'] = '10'
                    # set label:
                    s.attr['label'] = merge_table_pieces(content)
                
                # <---

            if 'components' in self.protocol_A.nodes[verb_a].keys(): # and type(self.protocol_A.nodes[a]) == 'protocols.models.Component':
                # Validate that reagent objectids are the same:


                if len(self.protocol_A.nodes[verb_a]['components']) ==0:
                    continue

                

                else:
                    # generate the diff content:   
                    components_a = [r['objectid'] for r in self.protocol_A.nodes[verb_a].children]
                    components_b = [r['objectid'] for r in self.protocol_B.nodes[verb_b].children]
                    
                    components_list_diff = set(r['objectid'] for r in self.protocol_A.nodes[verb_a].children) - set(r['objectid'] for r in self.protocol_B.nodes[verb_b].children)

                    if components_list_diff:
                        pass
                        # add a function that can tell the difference between different names
                    
                    else:
                        scores = [] # tracks the error rate of a matching components
                        content = [] # gets the html strings
                        for m,n in zip(components_a,components_b): 
                            d = DictDiffer (self.protocol_A.nodes[m].summary, self.protocol_B.nodes[n].summary)
                            scores.append((len(d.added()) + len(d.removed()) + len(d.changed())))
                            # print self.protocol_A.nodes[m]['objectid'], self.protocol_A.nodes[n]['objectid'], d.changed()
                            tmp = html_label_two_protocols(self.protocol_A.nodes[m].summary,self.protocol_B.nodes[n].summary,d.changed(), d.unchanged(), components = True) 
                            content.append(tmp)
                            
                    # --->  create a compare-graph-object that will apear between the 2 base diagrams:
                    if components:
                        print 'adding components layer'
                        diff_object = self.protocol_A.nodes[components_a[0]].pk 
                        ea = self.agraph.add_edge(self.protocol_A.nodes[verb_a].pk,diff_object)
                        eb = self.agraph.add_edge(self.protocol_B.nodes[verb_b].pk,diff_object)     
                        N = self.agraph.add_subgraph([self.protocol_A.nodes[verb_a].pk, diff_object, self.protocol_B.nodes[verb_b].pk], rank = 'same', rankdir='LR', name = self.protocol_A.nodes[verb_a].pk) #, name='%s'%(layer_names[nc])) 
                        
                        # set layout and colors
                        s = self.agraph.get_node(diff_object)
                        s.attr['shape'] = 'box'
                        s.attr['color'] = '#C0C0C0'
                        s.attr['style'] = 'rounded'
                        s.attr['fontsize'] = '10'
                        s.attr['label'] = merge_table_pieces(content, 'components')

            if 'thermocycle' in self.protocol_A.nodes[verb_a].keys():
                import itertools
                # generate the diff content:  

                # get all thermo children:
                phases_A = [r['objectid'] for r in self.protocol_A.nodes[verb_a].children]
                phases_B = [r['objectid'] for r in self.protocol_B.nodes[verb_b].children]

                match = set(phases_A) - set(phases_B)
                if len(match) == 0: 
                    # print 'len match = 0'
                # compare nested thermo objects:
                    table = []
                    for thermo in phases_A:
                        job_A = self.protocol_A.nodes[thermo].summary
                        job_B = self.protocol_B.nodes[thermo].summary
                        # print 'thermo is %s, \n A: %s + \n, B: %s'%(thermo, job_A['name'], job_B['name'])
                        d = DictDiffer(job_A, job_B)
                        if 'phases' in d.changed() or 'cycles' in d.changed():
                            # go through all items in both phases
                            it = itertools.izip(job_A['phases'], job_B['phases']) 
                            
                            for i,j in it: # getting the subphase name that is different
                                subphase_A = i
                                subphase_B = j
                                f = DictDiffer(subphase_A, subphase_B)
                                if f.changed():
                                    L = f.changed() 
                                    
                                    subphases = {}
                                    for each_subphase in L:
                                        # subphases[each_subphase] = [] 
                                        g = DictDiffer(subphase_A[each_subphase], subphase_B[each_subphase])    
                                        subphases[each_subphase] = g.changed()
                                        
                            
                            tmp = add_thermo(job_A, job_B, d.changed(), subphases)
                            table.append(tmp)
                            continue
                
                        if 'name' in d.changed():
                            print 'name changed'    

                        else:
                            tmp = add_thermo(job_A, job_B)
                            table.append(tmp)
                            
                    table = merge_table_pieces(table, 'thermocycle')        
                            
                 # --->  create a compare-graph-object that will apear between the 2 base diagrams:
                if thermocycle: 
                    print 'addinf thermo layer'
                    diff_object = self.protocol_A.nodes[phases_A[0]].pk 
                    ea = self.agraph.add_edge(self.protocol_A.nodes[verb_a].pk,diff_object)
                    eb = self.agraph.add_edge(self.protocol_B.nodes[verb_b].pk,diff_object)     
                    N = self.agraph.add_subgraph([self.protocol_A.nodes[verb_a].pk, diff_object, self.protocol_B.nodes[verb_b].pk], rank = 'same', rankdir='LR', name = self.protocol_A.nodes[verb_a].pk) #, name='%s'%(layer_names[nc])) 
                    
                    # set layout and colors
                    s = self.agraph.get_node(diff_object)
                    s.attr['shape'] = 'box'
                    s.attr['color'] = '#C0C0C0'
                    s.attr['style'] = 'rounded'
                    s.attr['fontsize'] = '10'
                    s.attr['label'] = (table)


        # if steps: 
        #     first_actions = [self.protocol_A.nodes[r]['objectid'] for r in self.protocol_A.get_steps]
        #     steps_a = [r for r in self.protocol_A.data['verbatim']]
        #     # steps_b = [r for r in self.protocol_B.data['verbatim']]  

        #     for i, step in enumerate(self.protocol_A.get_steps):       
        #         if step in first_action:
        #             self.agraph.add_node(self.protocol_A.nodes[step].pk)
        #             step_object = self.agraph.get_node(self.protocol_A.nodes[step].pk)
        #             # line in up with the first action of that step:
        #             ea = self.agraph.add_edge(self.protocol_A.nodes[step].children[0].pk, step_object)
        #             # eb = self.agraph.add_edge(self.protocol_B.nodes[step].children[0]['objectid'],step_object)
        #             N = self.agraph.add_subgraph([step_object, self.protocol_A.nodes[step].children[0].pk], rank = 'same', rankdir='LR') #, name='%s'%(layer_names[nc]))                 
            
        #             s = self.agraph.get_node(step_object)
        #             s.attr['shape'] = 'box'
        #             s.attr['color'] = '#C0C0C0'
        #             s.attr['style'] = 'rounded'
        #             s.attr['fontsize'] = '10'
        #             s.attr['label'] = steps_a[i]#merge_table_pieces(content, 'components')
    
        return self    


        # def add_step_layer(self): 



