from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import django.utils.simplejson as json
from compare.models import ProtocolPlot, DictDiffer, Compare, CompareVerb, CompareChildren
from django import http
from django.views.generic.detail import View, BaseDetailView, SingleObjectTemplateResponseMixin
from django.views.generic import TemplateView, View
from compare.utils import html_label_two_protocols, merge_table_pieces, add_step_label  
from django.core.urlresolvers import reverse
from protocols.models import Protocol
import itertools
from protocols.utils import MANUAL_VERBS


class CompareSelectView(TemplateView):
    template_name = "compare/compare_select.html"
    # GET THE PROTOCOLS THE USER CAN SEE
    def get_context_data(self, **kwargs):

        context = super(CompareSelectView, self).get_context_data(**kwargs)
        context['protocols'] = Protocol.objects.all()           # THIS NEEDS TO BE CHANGED SO THAT THE USER ONLY SEE WHAT THEY HVE PERMISSION TO SEE
        return context

    def post(self, request, *args, **kwargs):
        '''This is done to handle the two forms'''
        
        protocol_a = Protocol.objects.get(pk=int(request.POST['protocol_a']))
        protocol_b = Protocol.objects.get(pk=int(request.POST['protocol_b']))
        # NEED TO ADD CHECK TO MAKE SURE USER CAN SEE THESE PROTOCOLS

        url = reverse("compare_display_view", kwargs={'protocol_a_slug':protocol_a.slug, 'protocol_b_slug':protocol_b.slug})
        return HttpResponseRedirect(url)


class CompareDisplayView(CompareSelectView, TemplateView):          
    template_name = "compare/protocol_layout_api_headers.html"           

    def get_context_data(self, **kwargs):
        context = super(CompareDisplayView, self).get_context_data(**kwargs)
        return context 
        
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['protocol_a'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
        
        return self.render_to_response(context)    

class LayoutSingleView(TemplateView):
    template_name = "compare/protocol_layout_api_1_headers.html"           
    
    def get_context_data(self, **kwargs):

        context = super(LayoutSingleView, self).get_context_data(**kwargs)
        return context 
        
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['protocol_a'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])

        return self.render_to_response(context)    



# !!! DEPRECATED VIEWS::




# FONT_SIZE = '10'
# HTML_TARGET = '_top'
# COLOR_A = '#B82F3'
# COLOR_B = '#015666' 
# NODE_STYLE = 'solid' # "rounded" produces a longer svg filled with polylines. 

# class CompareBaseView(TemplateView):
#     # template_name = "compare/compare_default.html"

#     def get(self, request, *args, **kwargs):
#         '''Gets the context data'''
#         arguments={}
#         context = self.get_context_data()
#         nodes = ['thermo', 'machine', 'component', 'steps', 'manual']

#         protocol_a = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
#         context['protocol_a'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
#         context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
#         display = 'single'
#         arguments={'protocol_a_slug':context['protocol_a'].slug}              
        
#         if 'protocol_b_slug' in kwargs and kwargs['protocol_b_slug'] != 'layers':
            
#             context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
#             display = 'double'
#             arguments={'protocol_a_slug':context['protocol_a'].slug, 'protocol_b_slug':context['protocol_b'].slug}

#         # assemble JSON object for JS D3:
#         JSONdata = [protocol_a.nodes[r] for r in protocol_a.get_actions()]
        
#         # set position variables:
#         num_verbs = len(protocol_a.get_actions())
#         y_height = 30
#         y_spacer = 15
#         y_max = num_verbs * y_height + (num_verbs-1) * y_spacer
#         spacing = range(0,y_max, y_height + y_spacer)
#         y_position = dict((x,y) for x,y in zip(protocol_a.get_actions(),spacing))

#         # add URLS and y position to action 
#         for t in JSONdata:
#             t[u'url']= protocol_a.nodes[t['objectid']].action_update_url()
#             t[u'position'] = y_position[t['objectid']]
#             t[u'childtype'] = protocol_a.nodes[t['objectid']].childtype()


#         context['data'] = json.dumps(JSONdata)
#         context['steps'] = context['protocol_a'].steps 
#         context['position_data'] = json.dumps([y_height, y_spacer, y_max ])               
        
#         return self.render_to_response(context) #get_json_response(self.convert_context_to_json(JSONdata))



# class CompareLayersView(CompareBaseView, TemplateView):
#     template_name = "compare/protocol_basic.html"        

# class CompareBasePyGvView(TemplateView):
#     # template_name = "compare/compare_default.html"

#     def get(self, request, *args, **kwargs):
#         '''Gets the context data'''
#         arguments={}
#         context = self.get_context_data()
#         nodes = ['thermo', 'machine', 'component', 'steps', 'manual']

#         context['protocol_a'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
#         context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
#         display = 'single'
#         arguments={'protocol_a_slug':context['protocol_a'].slug}              
#         # template_name = "compare/single_base_default.html"
#         # render = 'compare_single'

#         if 'protocol_b_slug' in kwargs and kwargs['protocol_b_slug'] != 'layers':
            
#             context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
#             display = 'double'
#             arguments={'protocol_a_slug':context['protocol_a'].slug, 'protocol_b_slug':context['protocol_b'].slug}            
#             # template_name = "compare/compare_default.html" 
#             # render = 'compare_protocols' 
            
#         # else:
#         #     context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        
#         # if 'layers' in kwargs:
#         context['layers'] = kwargs['layers']        # CHECK IN THE TEMPLATE
#         layers = context['layers'].split('-')
#         render_layers = 'compare_layers'
#         # template_name = "compare/compare_layer.html" 
#         # render_base = 'compare_protocols'
        
#         if display == 'single':
#             render_layers = 'compare_single_layers'      
#             # template_name = "compare/single_base_default.html"
#             # render_base = 'compare_single'  
            
#         for node in nodes:
#             context['%s_layer' % node] = node in layers

#             if node in layers:
#                 node_list = [x for x in layers if x != node]
#             else:
#                 node_list = layers + [node]

#             if node_list:
#                 node_list.sort()
#                 arguments['layers']  = "-".join( node_list )
#                 context['%s_link' % node] = reverse(render_layers,  kwargs = arguments)
#                 # else:
#                 #     context['%s_link' % node] = reverse(render_base, kwargs = arguments)
#         # else:
#         #     for node in nodes:
#         #         context['%s_layer' % node] = False
#         #         arguments['layers']  = node
#         #         render_layers = 'compare_add_layers'
#         #         if display == 'single':
#         #             render_layers = 'compare_single_layers' 
#         #         context['%s_link' % node] = reverse(render_layers, kwargs=arguments )

#         print 'returning CompareBaseView'
#         return self.render_to_response(context)


# class CompareLayersPyGvView(CompareBasePyGvView):
#     template_name = "compare/compare_layers.html"


# class CompareLayersGraphicPyGvView(View):
#     #template_name = "compare/comapare_layer.html"
#     '''
#         Adds a compare layer to Returns a graphic representaion of a comparison in either a SVG or PNG format.
#     '''
    
#     def get(self, request, *args, **kwargs):
#         '''Gets the context data'''

#         protocol_a = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
#         if 'protocol_b_slug' in kwargs:
#             protocol_b = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
#         else:
#             protocol_b = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])    
#         layers = kwargs['layers']
#         format = "svg"

#         grapher = Grapher(protocol_a, protocol_b, "svg")
#         base = grapher.draw_two_protocols()
#         layer = base.add_diff_layer(layers = layers)
#         img = layer.agraph.draw(prog='dot', format="svg")    

#         if format in ['svg']:
#             format = format + "+xml"

#         response = HttpResponse(img, mimetype='image/%s' % format)
#         # print 'returning ComparelayersGraphicView'
#         return response

# class CompareSingleLayersPyGvView(CompareBasePyGvView):
    
#     template_name = "compare/compare_single_layers.html"
#     # print template_name

# class CompareSingleLayersGraphicPyGvView(View):
#     '''
#     Returns a graphic representaion of a single protocol in SVG or PNG format.
#     '''

#     def get(self, request, *args, **kwargs):
#         '''Gets the context data'''

#         protocol_a = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
#         format = kwargs['format']
#         layers = None

#         if 'layers' in kwargs:
#             layers = kwargs['layers']
#         # grapher = Grapher(protocol_a, protocol_b, format)
#         grapher = Grapher(protocol_a, format=format)
#         base = grapher.draw_two_protocols()
#         layer = base.add_layers_routine(layers = layers)
#         img = layer.agraph.draw(prog='dot', format="svg")    

#         if format in ['svg']:
#             format = format + "+xml"

#         response = HttpResponse(img, mimetype='image/%s' % format)
#         return response                

# class Grapher(object):
#     def __init__(self, protocol_a, protocol_b = None, format="svg", **kwargs):
#         import pygraphviz as pgv

#         self.agraph = pgv.AGraph(ranksep = '0.2')
#         self.agraph.graph_attr['clusterrank'] = 'local' # do not remove this line
#         self.protocol_A = protocol_a
#         self.A_pk = [self.protocol_A.nodes[r].pk for r in self.protocol_A.get_actions()]
#         self.flags = {}
        
#         if protocol_b == None:
#             self.protocol_B = protocol_a
#             self.B_pk = [self.protocol_A.nodes[r].pk for r in self.protocol_A.get_actions()]
#             self.flags['steps'] = True
#         else:
#             self.protocol_B = protocol_b    
#             self.B_pk = [self.protocol_B.nodes[r].pk for r in self.protocol_B.get_actions()]
#             self.flags['steps'] = False

#         # find all actions common to both protocols:    
#         self.both = set(self.protocol_A.get_actions()).intersection(set(self.protocol_B.get_actions()))
#         # alls = set(self.protocol_A.get_actions()).union(set(self.protocol_B.get_actions()))
#         # Set the pair names using the .pk index for graph node naming
#         self.pairs = [(self.protocol_A.nodes[r].pk, self.protocol_B.nodes[r].pk) for r in self.both]
#         # set the unaligned verbs:
#         self.a_unique = set(self.protocol_A.get_actions())-set(self.protocol_B.get_actions())
#         self.b_unique = set(self.protocol_B.get_actions())-set(self.protocol_A.get_actions())


#     def draw_two_protocols(self, **kwargs):
#         ''' this function draws out 2 base protocols as a sequence of actions. 
#             add_layers_routine(layers = 'none-manual') adds the specified layers that a user wants to compare'''

#         # Draw out the first protocol:
#         self.layers = []    
#         for i in range(1, len(self.A_pk)):
            
#             self.agraph.add_edge(self.A_pk[i-1], self.A_pk[i])
#             e = self.agraph.get_edge(self.A_pk[i-1], self.A_pk[i])
#             e.attr['style'] = 'setlinewidth(9)' 
#             e.attr['color'] = COLOR_A
#             n=self.agraph.get_node(self.A_pk[i])
#             n.attr['shape']='box'
#             n.attr['fontsize'] = FONT_SIZE
#             n.attr['style'] = NODE_STYLE
#             n.attr['height'] = '0.2'
#             node_object = self.protocol_A.nodes[self.protocol_A.get_actions()[i]]
#             n.attr['label']= node_object['verb'] #+ '_' + self.protocol_A.nodes[self.protocol_A.get_actions()[i]].pk
#             # n.attr['URL'] = node_object.get_absolute_url()
#             # n.attr['target'] = HTML_TARGET
                
#         # Set the 0'th node and title in protocol_A 
#         n = self.agraph.get_node(self.A_pk[0])
#         n.attr['shape']='box'
#         n.attr['fontsize'] = FONT_SIZE
#         n.attr['style'] = NODE_STYLE
#         n.attr['height'] = '0.2'
#         node_object = self.protocol_A.nodes[self.protocol_A.get_actions()[0]]
#         n.attr['label']=node_object['verb'] 
#         # n.attr['URL'] = node_object.get_absolute_url()
#         # n.attr['target'] = HTML_TARGET
        
#         # add base of second protocol:
#         for i in range(1, len(self.B_pk)):
#             self.agraph.add_edge(self.B_pk[i-1], self.B_pk[i])
#             # print 'drawing protocol %s'% self.protocol_B.name
#             e = self.agraph.get_edge(self.B_pk[i-1], self.B_pk[i])
#             e.attr['style'] = 'setlinewidth(9)' 
#             e.attr['color'] = COLOR_B
#             n=self.agraph.get_node(self.B_pk[i])
#             n.attr['shape']='box'
#             n.attr['fontsize'] = FONT_SIZE
#             n.attr['style'] = NODE_STYLE
#             n.attr['height'] = '0.2'
#             node_object = self.protocol_B.nodes[self.protocol_B.get_actions()[i]]
#             n.attr['label']= node_object['verb'] 
#             # n.attr['URL'] = node_object.get_absolute_url()    
#             # n.attr['target'] = HTML_TARGET
#         # Set the 0'th node in  protocol_A  
#         n = self.agraph.get_node(self.B_pk[0])
#         n.attr['shape']='box'
#         n.attr['fontsize'] = FONT_SIZE
#         n.attr['style'] = NODE_STYLE
#         n.attr['height'] = '0.2'
#         node_object = self.protocol_B.nodes[self.protocol_B.get_actions()[0]]
#         n.attr['label']= node_object['verb'] 
#         # n.attr['URL'] = node_object.get_absolute_url()
#         # n.attr['target'] = HTML_TARGET

#         for j in self.pairs:
#             N = self.agraph.add_subgraph(j, name =str(j[0][j[0].index('-')+1:]), rank='same', rankdir='LR')

#         return self    
    
#     def add_layers_routine(self, **kwargs):
#         ''' this function adds layers on the three groups of subgraphs that control the verb alignment in this view: 
#         paired --> verb_a.pk -- diff_object.pk -- verb_b.pk
#         single_left --> verb_a.pk -- diff_object.pk 
#         single_right -->  diff_object.pk -- verb_b.pk
#         it currently adds these layers:
#             'manual',
#             'machines'
#             'components'
#             'thermocycle'
#             'steps' - displays verbatim text. '''

#         if 'layers' in kwargs.keys():
#             self.layers = kwargs['layers'].split('-')

#         self.add_node_object(self.both, ref_protocol = self.protocol_A)

#         # these lists contain a few or no nodes:
#         if self.a_unique:
#             self.flags['position'] = 'right'
#             self.add_node_object(self.a_unique, ref_protocol = self.protocol_A, position = 'right')
#         if self.b_unique:
#             self.flags['position'] = 'left'
#             self.add_node_object(self.b_unique, ref_protocol = self.protocol_B, position = 'left')

#         return self    


#     def add_node_object(self, node_group, ref_protocol = None, **kwargs): # , machines = True, components = True, thermocycle = True
        
#         if 'position' in kwargs:
#             pass

#         for j in node_group:
#             # identify the type of layer
#             if 'machine' in ref_protocol.nodes[j] and 'machine' in self.layers:
#                 if not self.add_machine_layer(j, ref_protocol):
#                     continue

#             if ref_protocol.nodes[j]['verb'] in MANUAL_VERBS and 'manual' in self.layers:    
#                 if not self.add_manual_layer(j, ref_protocol):
#                     continue

#             if 'components' in ref_protocol.nodes[j] and 'components' in self.layers:     
#                 if not self.add_components_layer(j, ref_protocol):
#                     continue

#             if 'thermocycle' in ref_protocol.nodes[j] and 'thermo' in self.layers:                 
#                 if not self.add_thermocycle_layer(j, ref_protocol):
#                     continue

#     def add_machine_layer(self, j, ref_protocol):
#         layer = 'machine'
#         node_object = ref_protocol.nodes[j]['machine']
#         URL = node_object.get_update_url()
#         diff_object = ref_protocol.nodes[j]['machine'].pk
#         if 'position' in self.flags:
#             if self.flags['position'] == 'right':
#                 x = ref_protocol.nodes[j]['machine'].summary
#                 y = x

#             if self.flags['position'] == 'left':
#                 y =  ref_protocol.nodes[j]['machine'].summary   
#                 x = y
        
#         else: 
#             x = self.protocol_A.nodes[j]['machine'].summary
#             y = self.protocol_B.nodes[j]['machine'].summary
        
#         d = DictDiffer (x, y)
#         content = html_label_two_protocols(x,y,d.changed(name = True, objectid = True, slug = True), d.unchanged(), current_layer = layer) 
#         self.style_content(j, URL, diff_object, content)

#     def add_manual_layer(self, j, ref_protocol):
#         layer = 'manual'
#         node_object = ref_protocol.nodes[j]
#         URL = node_object.action_update_url()
#         diff_object = ref_protocol.nodes[j].pk + '_manual'
#         if 'position' in self.flags:
#             if self.flags['position'] == 'right':
#                 x = ref_protocol.nodes[j].summary
#                 y = x

#             if self.flags['position'] == 'left':
#                 y =  ref_protocol.nodes[j].summary   
#                 x = y    
        
#         else:        
#             x = self.protocol_A.nodes[j].summary
#             y = self.protocol_B.nodes[j].summary  
        
#         d = DictDiffer (x, y)
#         content = html_label_two_protocols(x,y,d.changed(name = True, objectid = True, slug = True), d.unchanged(), current_layer = layer)   
#         self.style_content(j, URL, diff_object, content)

#     def add_components_layer(self, j, ref_protocol):
#         layer = 'components'

#         # Validate that reagent objectids are the same:

#         if len(ref_protocol.nodes[j]['components']) == 0:
#             return None
#         else:
#             node_object = ref_protocol.nodes[j]
#             URL ='None'

#             if 'position' in self.flags:
#                 if self.flags['position'] == 'right':
#                     x = [r['objectid'] for r in self.protocol_A.nodes[j].children]
#                     y = x

#                 if self.flags['position'] == 'left':
#                     y = [r['objectid'] for r in self.protocol_B.nodes[j].children] 
#                     x = y 

#             else:        
#             # generate the diff content:   
#                 x = [r['objectid'] for r in self.protocol_A.nodes[j].children]
#                 y = [r['objectid'] for r in self.protocol_B.nodes[j].children]
            
#             diff_object = ref_protocol.nodes[x[0]].pk 
#             scores = [] # tracks the error rate of a matching components
#             content = [] # gets the html strings
#             for m,n in zip(x,y): 
#                 d = DictDiffer (self.protocol_A.nodes[m].summary, self.protocol_B.nodes[n].summary)
#                 scores.append((len(d.added()) + len(d.removed()) + len(d.changed())))
#                 # print self.protocol_A.nodes[m]['objectid'], self.protocol_A.nodes[n]['objectid'], d.changed()
#                 tmp = html_label_two_protocols(self.protocol_A.nodes[m].summary,self.protocol_B.nodes[n].summary,d.changed(), d.unchanged(), current_layer = layer) 
#                 content.append(tmp)      
            
#             self.style_content(j, URL, diff_object, content, current_layer = layer)    

#     def add_thermocycle_layer(self, j, ref_protocol):
#         layer = 'thermocycle'
#         if len(ref_protocol.nodes[j]['thermocycle']) == 0:
#             return None
#         else:
#             # generate the diff content:   
#             x = [r['objectid'] for r in self.protocol_A.nodes[j].children]
#             y = [r['objectid'] for r in self.protocol_B.nodes[j].children]
            
#             scores = [] # tracks the error rate of a matching components
#             content = [] # gets the html strings
#             for m,n in zip(x,y): 
#                 d = DictDiffer (self.protocol_A.nodes[m].summary, self.protocol_B.nodes[n].summary)
#                 scores.append((len(d.added()) + len(d.removed()) + len(d.changed())))
#                 # print self.protocol_A.nodes[m]['objectid'], self.protocol_A.nodes[n]['objectid'], d.changed()
#                 tmp = html_label_two_protocols(self.protocol_A.nodes[m].summary,self.protocol_B.nodes[n].summary,d.changed(), d.unchanged(), current_layer = layer) 
#                 content.append(tmp)

#             diff_object = ref_protocol.nodes[x[0]].pk 
#             URL = None
#             self.style_content(j, URL, diff_object, content, current_layer = layer)  

#         # for j in self.a_unique:               
                    

                
#     def style_content(self, j, URL, diff_object, content, current_layer = None):

#         try:
#             N = self.agraph.get_subgraph(str(j))
#             if len(N.nodes()) == 2:
#                 (verb_object_a, verb_object_b) = N.nodes()
#                 N.add_node(diff_object)        
#                 self.agraph.add_edge(verb_object_a,diff_object)
#                 self.agraph.add_edge(diff_object, verb_object_b)    

#         except AttributeError:
#             if self.flags['position'] == 'right':
#                 verb_object_a = self.protocol_A.nodes[j].pk
#                 self.agraph.add_edge(verb_object_a,diff_object)
#                 subgraph = [verb_object_a, diff_object]

#             if self.flags['position'] == 'left':    
#                 verb_object_b = self.protocol_B.nodes[j].pk
#                 self.agraph.add_edge(diff_object, verb_object_b)
#                 subgraph = [diff_object, verb_object_b]

#             N = self.agraph.add_subgraph(subgraph, name =str(j), rank='same', rankdir='LR')    
          
#         s = self.agraph.get_node(diff_object)
#         s.attr['shape'] = 'box'
#         s.attr['color'] = '#C0C0C0'
#         s.attr['style'] = NODE_STYLE
#         s.attr['fontsize'] = FONT_SIZE  

#         # set label:
#         s.attr['label'] = merge_table_pieces(content, current_layer)

#         # if current_layer == 'manual':
#         #     node_object = self.protocol_A.nodes[j]
#         #     s.attr['URL'] = node_object.action_update_url()

#         # else:
#         #     node_object = self.protocol_A.nodes[j][current_layer]
#         #     s.attr['URL'] = node_object.get_update_url()    
#         s.attr['URL'] = URL

#         s.attr['target'] = HTML_TARGET      

#     