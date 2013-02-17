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
        context = self.get_context_data()

        protocol_a = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        protocol_b = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
        format = kwargs['format']


        # NEED TO REPLACE THE BELOW RESPONSE WITH ONE USING STRINGIO
        return self.render_to_response(context)

