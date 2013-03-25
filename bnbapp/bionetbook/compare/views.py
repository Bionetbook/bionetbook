from django.http import HttpResponse, HttpResponseRedirect
from compare.models import ProtocolPlot, DictDiffer
from django.views.generic import TemplateView, View
from compare.utils import html_label_two_protocols, merge_table_pieces, add_step_label  
from django.core.urlresolvers import reverse
from protocols.models import Protocol


class CompareSelectView(TemplateView):
    template_name = "compare/compare_select.html"

    # GET THE PROTOCOLS THE USER CAN SEE
    def get_context_data(self, **kwargs):

        context = super(CompareSelectView, self).get_context_data(**kwargs)
        context['protocols'] = Protocol.objects.all()           # THIS NEEDS TO BE CHANGED SO THAT THE USER ONLY SEE WHAT THEY HVE PERMISSION TO SEE
        return context

    def post(self, request, *args, **kwargs):
        '''This is done to handle the two forms'''
        protocol_a = Protocol.objects.get(pk=request.POST['protocol_a'][0])
        protocol_b = Protocol.objects.get(pk=request.POST['protocol_b'][0])

        # NEED TO ADD CHECK TO MAKE SURE USER CAN SEE THESE PROTOCOLS

        url = reverse("compare_layers", kwargs={'protocol_a_slug':protocol_a.slug, 'protocol_b_slug':protocol_b.slug, 'layers':'none'})
        return HttpResponseRedirect(url)



class CompareBaseView(TemplateView):
    # template_name = "compare/compare_default.html"

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''
        arguments={}
        context = self.get_context_data()
        nodes = ['thermo', 'machine', 'component', 'steps']

        context['protocol_a'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        display = 'single'
        arguments={'protocol_a_slug':context['protocol_a'].slug}              
        # template_name = "compare/single_base_default.html"
        # render = 'compare_single'
        
        

        if 'protocol_b_slug' in kwargs and kwargs['protocol_b_slug'] != 'layers':
            
            context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
            display = 'double'
            arguments={'protocol_a_slug':context['protocol_a'].slug, 'protocol_b_slug':context['protocol_b'].slug}            
            # template_name = "compare/compare_default.html" 
            # render = 'compare_protocols' 
            
        # else:
        #     context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        
        # if 'layers' in kwargs:
        context['layers'] = kwargs['layers']        # CHECK IN THE TEMPLATE
        layers = context['layers'].split('-')
        render_layers = 'compare_layers'
        # template_name = "compare/compare_layer.html" 
        # render_base = 'compare_protocols'
        
        
        if display == 'single':
            render_layers = 'compare_single_layers'      
            # template_name = "compare/single_base_default.html"
            # render_base = 'compare_single'  
            
        for node in nodes:
            context['%s_layer' % node] = node in layers

            if node in layers:
                node_list = [x for x in layers if x != node]
            else:
                node_list = layers + [node]

            if node_list:
                node_list.sort()
                arguments['layers']  = "-".join( node_list )
                context['%s_link' % node] = reverse(render_layers,  kwargs = arguments)
                # else:
                #     context['%s_link' % node] = reverse(render_base, kwargs = arguments)
        # else:
        #     for node in nodes:
        #         context['%s_layer' % node] = False
        #         arguments['layers']  = node
        #         render_layers = 'compare_add_layers'
        #         if display == 'single':
        #             render_layers = 'compare_single_layers' 
        #         context['%s_link' % node] = reverse(render_layers, kwargs=arguments )

        print 'returning CompareBaseView'
        return self.render_to_response(context)


# class CompareBaseGraphicView(View):
#     '''
#     Returns a graphic representaion of a comparison in either a SVG or PNG format.
#     '''

#     def get(self, request, *args, **kwargs):
#         '''Gets the context data'''

#         protocol_a = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])

#         if 'protocol_b_slug' in kwargs:
#             protocol_b = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
#         else:
#             protocol_b = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])    
        
#         format = kwargs['format']
#         grapher = Grapher(protocol_a, protocol_b, format)
#         base = grapher.draw_two_protocols()
#         img = base.agraph.draw(prog='dot', format=format)    

#         if format in ['svg']:
#             format = format + "+xml"

#         response = HttpResponse(img, mimetype='image/%s' % format)
#         print 'returning CompareBaseGraphicView'
#         return response


class CompareLayersView(CompareBaseView):
    template_name = "compare/compare_layers.html"


class CompareLayersGraphicView(View):
    #template_name = "compare/comapare_layer.html"
    '''
        Adds a compare layer to Returns a graphic representaion of a comparison in either a SVG or PNG format.
    '''
    
    def get(self, request, *args, **kwargs):
        '''Gets the context data'''

        protocol_a = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        if 'protocol_b_slug' in kwargs:
            protocol_b = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
        else:
            protocol_b = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])    
        layers = kwargs['layers']
        format = "svg"

        grapher = Grapher(protocol_a, protocol_b, "svg")
        base = grapher.draw_two_protocols()
        layer = base.add_diff_layer(layers = layers)
        img = layer.agraph.draw(prog='dot', format="svg")    

        if format in ['svg']:
            format = format + "+xml"

        response = HttpResponse(img, mimetype='image/%s' % format)
        # print 'returning ComparelayersGraphicView'
        return response

class CompareSingleLayersView(CompareBaseView):
    
    template_name = "compare/compare_single_layers.html"
    # print template_name

class CompareSingleLayersGraphicView(View):
    '''
    Returns a graphic representaion of a single protocol in SVG or PNG format.
    '''

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''

        protocol_a = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        format = kwargs['format']
        layers = None

        if 'layers' in kwargs:
            layers = kwargs['layers']
        # grapher = Grapher(protocol_a, protocol_b, format)
        grapher = Grapher(protocol_a, format=format)
        base = grapher.draw_two_protocols()
        layer = base.add_diff_layer(layers = layers)
        img = layer.agraph.draw(prog='dot', format="svg")    

        if format in ['svg']:
            format = format + "+xml"

        response = HttpResponse(img, mimetype='image/%s' % format)
        # print 'returning SingleLayersGraphicView'
        return response                


class Grapher(object):
    def __init__(self, protocol_a, protocol_b = None, format="svg", **kwargs):
        import pygraphviz as pgv

        self.agraph = pgv.AGraph(ranksep = '0.2')
        self.agraph.graph_attr['clusterrank'] = 'local' # do not remove this line
        self.protocol_A = protocol_a
        self.A_pk = [self.protocol_A.nodes[r].pk for r in self.protocol_A.get_actions]
        
        if protocol_b == None:
            self.protocol_B = protocol_a
            self.B_pk = [self.protocol_A.nodes[r].pk for r in self.protocol_A.get_actions]
        else:
            self.protocol_B = protocol_b    
            self.B_pk = [self.protocol_B.nodes[r].pk for r in self.protocol_B.get_actions]
         # list of actions in pk-objectid format
        # self.B_pk = [self.protocol_B.nodes[r].pk for r in self.protocol_B.get_actions]
        self.matching_verbs_pk = zip(self.A_pk,self.B_pk)
        self.matching_verbs = zip(self.protocol_A.get_actions, self.protocol_B.get_actions)
        self.format = format

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
            n.attr['height'] = '0.2'
            node_object = self.protocol_A.nodes[self.protocol_A.get_actions[i]]
            n.attr['label']= node_object['verb'] #+ '_' + self.protocol_A.nodes[self.protocol_A.get_actions[i]].pk

            # if 'call_for_protocol' in node_object:
            n.attr['URL'] = node_object.get_absolute_url()
            n.attr['target'] = '_top'
                

        # Set the 0'th node and title in protocol_A 
        n = self.agraph.get_node(self.matching_verbs_pk[0][0])
        
        n.attr['shape']='box'
        n.attr['fontsize'] = '10'
        n.attr['style'] = 'rounded'
        n.attr['height'] = '0.2'
        node_object = self.protocol_A.nodes[self.protocol_A.get_actions[0]]
        n.attr['label']=node_object['verb'] 
        n.attr['URL'] = node_object.get_absolute_url()
        n.attr['target'] = '_top'
        
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
            n.attr['height'] = '0.2'
            node_object = self.protocol_B.nodes[self.protocol_B.get_actions[i]]
            n.attr['label']= node_object['verb'] 
            n.attr['URL'] = node_object.get_absolute_url()    
            n.attr['target'] = '_top'
        # Set the 0'th node in  protocol_A  
        n = self.agraph.get_node(self.matching_verbs_pk[0][1])
        n.attr['shape']='box'
        n.attr['fontsize'] = '10'
        n.attr['style'] = 'rounded'
        n.attr['height'] = '0.2'
        node_object = self.protocol_B.nodes[self.protocol_B.get_actions[0]]
        n.attr['label']= node_object['verb'] 
        n.attr['URL'] = node_object.get_absolute_url()
        n.attr['target'] = '_top'
        return self
    

    def add_step_layer(self, verb_a, verb_b, verb_object_a, verb_object_b, diff_object = None): 
            first_actions_a = [self.protocol_A.nodes[r].children[0]['objectid'] for r in self.protocol_A.get_steps]
            first_actions_b = [self.protocol_A.nodes[r].children[0]['objectid'] for r in self.protocol_B.get_steps]
            steps_a = [r for r in self.protocol_A.data['verbatim']]
            steps_b = [r for r in self.protocol_A.data['verbatim']]
            if verb_a in first_actions_a: # or verb_b in first_actions_b  
                

                self.agraph.add_node(self.protocol_A.nodes[self.protocol_A.nodes[verb_a].parent['objectid']].pk)
                self.agraph.add_node(self.protocol_B.nodes[self.protocol_B.nodes[verb_b].parent['objectid']].pk)
                step_object_a = self.agraph.get_node(self.protocol_A.nodes[self.protocol_A.nodes[verb_a].parent['objectid']].pk)
                step_object_b = self.agraph.get_node(self.protocol_B.nodes[self.protocol_B.nodes[verb_b].parent['objectid']].pk)

                self.agraph.add_edge(step_object_a,verb_object_a)
                self.agraph.add_edge(step_object_b,verb_object_b)

                eas = self.agraph.get_edge(step_object_a, verb_object_a)
                ebs = self.agraph.get_edge(step_object_b, verb_object_b)

                
                if diff_object == None:
                    N = self.agraph.add_subgraph([step_object_a, verb_object_a, verb_object_b, step_object_b], rank = 'same', rankdir='LR')#) #, name='%s'%(layer_names[nc])) name = self.protocol_A.nodes[verb_a].pk, 
                else:
                    N = self.agraph.add_subgraph([step_object_a, verb_object_a, diff_object, verb_object_b, step_object_b], rank = 'same', rankdir='LR')#) #, name='%s'%(layer_names[nc])) name = self.protocol_A.nodes[verb_a].pk,
                
                sa = self.agraph.get_node(step_object_a)
                sa.attr['shape'] = 'box'
                sa.attr['color'] = '#C0C0C0'
                sa.attr['style'] = 'rounded'
                sa.attr['fontsize'] = '10'
                VERBATIM_A = self.protocol_A.data['verbatim'] 
                PARENT_A = self.protocol_A.nodes[verb_a].parent['objectid'] 
                sa.attr['label'] = add_step_label(VERBATIM_A[self.protocol_A.get_steps.index(PARENT_A)])

                sb = self.agraph.get_node(step_object_b)
                sb.attr['shape'] = 'box'
                sb.attr['color'] = '#C0C0C0'
                sb.attr['style'] = 'rounded'
                sb.attr['fontsize'] = '10'
                # sb.attr['width'] = '0.15'
                VERBATIM_B = self.protocol_A.data['verbatim'] 
                PARENT_B = self.protocol_B.nodes[verb_b].parent['objectid'] 
                sb.attr['label'] = add_step_label(VERBATIM_B[self.protocol_B.get_steps.index(PARENT_B)], step_layer = True)

    def add_diff_layer(self, **kwargs): # , machines = True, components = True, thermocycle = True
        ''' this function assumes that the pairs of objects are equivalent in that both have validated:
            'machines'
            'components'
            'thermocycle'
            'steps' - displays verbatim text. '''
        
        if 'layers' in kwargs.keys():
            layers = kwargs['layers'].split('-')

            
        for verb_a,verb_b in self.matching_verbs: #[(node_a, node_b), ]
            # print verb_a, verb_b
            if 'machine' in self.protocol_A.nodes[verb_a].keys() and 'machine' in layers:
                x = self.protocol_A.nodes[verb_a]['machine'].summary
                y = self.protocol_B.nodes[verb_b]['machine'].summary
                d = DictDiffer (x, y)
                content = html_label_two_protocols(x,y,d.changed(name = True, objectid = True, slug = True), d.unchanged(), machine = True) 


                self.agraph.add_node(self.protocol_A.nodes[verb_a].pk)
                self.agraph.add_node(self.protocol_B.nodes[verb_b].pk)
                verb_object_a = self.agraph.get_node(self.protocol_A.nodes[verb_a].pk)
                verb_object_b = self.agraph.get_node(self.protocol_B.nodes[verb_b].pk)

                diff_object = self.protocol_A.nodes[verb_a]['machine'].pk
                self.agraph.add_edge(verb_object_a,diff_object)
                self.agraph.add_edge(verb_object_b,diff_object)

                if 'steps' in layers:
                    self.add_step_layer(verb_a, verb_b, verb_object_a, verb_object_b, diff_object= diff_object)
                else:    
                    N = self.agraph.add_subgraph([verb_object_a, diff_object, verb_object_b], rank = 'same', name = self.protocol_A.nodes[verb_a].pk, rankdir='LR')#) #, name='%s'%(layer_names[nc])) 
                           # set layout and colors
                s = self.agraph.get_node(diff_object)
                s.attr['shape'] = 'box'
                s.attr['color'] = '#C0C0C0'
                s.attr['style'] = 'rounded'
                s.attr['fontsize'] = '10'
                # set label:
                s.attr['label'] = merge_table_pieces(content)

            if 'components' in self.protocol_A.nodes[verb_a].keys() and 'component' in layers: # and type(self.protocol_A.nodes[a]) == 'protocols.models.Component':
                # Validate that reagent objectids are the same:


                if len(self.protocol_A.nodes[verb_a]['components']) == 0:
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
                    self.agraph.add_node(self.protocol_A.nodes[verb_a].pk)
                    self.agraph.add_node(self.protocol_B.nodes[verb_b].pk)
                    verb_object_a = self.agraph.get_node(self.protocol_A.nodes[verb_a].pk)
                    verb_object_b = self.agraph.get_node(self.protocol_B.nodes[verb_b].pk)

                    diff_object = self.protocol_A.nodes[components_a[0]].pk 
                    ea = self.agraph.add_edge(verb_object_b, diff_object)
                    eb = self.agraph.add_edge(verb_object_a, diff_object)     
                    

                    if 'steps' in layers:
                        self.add_step_layer(verb_a, verb_b, verb_object_a, verb_object_b, diff_object= diff_object)
                    else:    
                        N = self.agraph.add_subgraph([verb_object_a, diff_object, verb_object_b], rank = 'same', name = self.protocol_A.nodes[verb_a].pk, rankdir='LR')#) #, name='%s'%(layer_names[nc])) 
                    # set layout and colors
                    s = self.agraph.get_node(diff_object)
                    s.attr['shape'] = 'box'
                    s.attr['color'] = '#C0C0C0'
                    s.attr['style'] = 'rounded'
                    s.attr['fontsize'] = '10'
                    s.attr['label'] = merge_table_pieces(content, 'components')

            if 'thermocycle' in self.protocol_A.nodes[verb_a].keys() and 'thermo' in layers: 


                if len(self.protocol_A.nodes[verb_a]['thermocycle']) == 0:
                    continue
                else:
                    # generate the diff content:   
                    thermo_a = [r['objectid'] for r in self.protocol_A.nodes[verb_a].children]
                    thermo_b = [r['objectid'] for r in self.protocol_B.nodes[verb_b].children]
                    
                    # components_list_diff = set(r['objectid'] for r in self.protocol_A.nodes[verb_a].children) - set(r['objectid'] for r in self.protocol_B.nodes[verb_b].children)

                    # if components_list_diff:
                    #     pass
                        # add a function that can tell the difference between different names
                    
                    # else:
                    scores = [] # tracks the error rate of a matching components
                    content = [] # gets the html strings
                    for m,n in zip(thermo_a,thermo_b): 
                        d = DictDiffer (self.protocol_A.nodes[m].summary, self.protocol_B.nodes[n].summary)
                        scores.append((len(d.added()) + len(d.removed()) + len(d.changed())))
                        # print self.protocol_A.nodes[m]['objectid'], self.protocol_A.nodes[n]['objectid'], d.changed()
                        tmp = html_label_two_protocols(self.protocol_A.nodes[m].summary,self.protocol_B.nodes[n].summary,d.changed(), d.unchanged(), thermocycle = True) 
                        content.append(tmp)
                            
                    # --->  create a compare-graph-object that will apear between the 2 base diagrams:
                    self.agraph.add_node(self.protocol_A.nodes[verb_a].pk)
                    self.agraph.add_node(self.protocol_B.nodes[verb_b].pk)
                    verb_object_a = self.agraph.get_node(self.protocol_A.nodes[verb_a].pk)
                    verb_object_b = self.agraph.get_node(self.protocol_B.nodes[verb_b].pk)

                    diff_object = self.protocol_A.nodes[thermo_a[0]].pk 
                    ea = self.agraph.add_edge(verb_object_b, diff_object)
                    eb = self.agraph.add_edge(verb_object_a, diff_object)     
                    

                    if 'steps' in layers:
                        self.add_step_layer(verb_a, verb_b, verb_object_a, verb_object_b, diff_object= diff_object)
                    else:    
                        N = self.agraph.add_subgraph([verb_object_a, diff_object, verb_object_b], rank = 'same', name = self.protocol_A.nodes[verb_a].pk, rankdir='LR')#) #, name='%s'%(layer_names[nc])) 
                    # set layout and colors
                    s = self.agraph.get_node(diff_object)
                    s.attr['shape'] = 'box'
                    s.attr['color'] = '#C0C0C0'
                    s.attr['style'] = 'rounded'
                    s.attr['fontsize'] = '10'
                    s.attr['label'] = merge_table_pieces(content, 'thermocycle')
    
        return self 

        