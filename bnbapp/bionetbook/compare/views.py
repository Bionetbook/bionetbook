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
        import pygraphviz as P

        protocol_a = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        protocol_b = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
        format = kwargs['format']

        A=P.AGraph() # init empty graph
        # set some default node attributes
        A.node_attr['style']='filled'
        A.node_attr['shape']='circle'
        # Add edges (and nodes)
        A.add_edge(1,2)
        A.add_edge(2,3)
        A.add_edge(1,3)
        A.layout() # layout with default (neato)
        img=A.draw(format=format) # draw png

        if format in ['svg']:
            format = format + "+xml"

        response = HttpResponse(img, mimetype='image/%s' % format)
        return response

