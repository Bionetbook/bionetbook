from django.http import HttpResponse
from compare.models import ProtocolPlot
from django.views.generic import TemplateView, View


class CompareView(TemplateView):
    template_name = "compare/compare_default.html"

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''
        context = self.get_context_data()

        context['protocol_a'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])

        return self.render_to_response(context)


class CompareGraphicView(View):
    '''
    Returns a graphic representaion of a comparison in either a SVG or PNG format.
    '''

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''

        protocol_a = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        protocol_b = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
        format = kwargs['format']

        grapher = Grapher(protocol_a, protocol_b, format)
        img = grapher.draw()

        if format in ['svg']:
            format = format + "+xml"

        response = HttpResponse(img, mimetype='image/%s' % format)
        return response


class Grapher(object):
    def __init__(self, protocol_a, protocol_b, format="svg"):
        import pygraphviz as P

        self.graph = P.AGraph()
        self.protocol_a = protocol_a
        self.protocol_b = protocol_b
        self.format = format

    def draw(self):
        # set some default node attributes
        self.graph.node_attr['style']='filled'
        self.graph.node_attr['shape']='circle'
        # Add edges (and nodes)
        self.graph.add_edge(1,2)
        self.graph.add_edge(2,3)
        self.graph.add_edge(1,3)
        self.graph.layout() # layout with default (neato)
        return self.graph.draw(format=self.format) # draw png



