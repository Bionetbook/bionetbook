# from django.http import HttpResponse
# from compare.models import ProtocolPlot
# import pygraphviz as agraph
from django.views.generic import TemplateView


class CompareView(TemplateView):
    template_name = "compare/compare_default.html"

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''
        context = self.get_context_data()

        context['protocol_a'] = kwargs['protocol_a_slug']
        context['protocol_b'] = kwargs['protocol_b_slug']

        return self.render_to_response(context)





# def protocol_plot(request, protocol_slug):

# 	# svg_plot = None
# 	# GET THE PROTOCOL
# 	protocol = ProtocolPlot.objects.get(slug__icontains=protocol_slug)
	
# 	# svg_data = protocol.get_svg()
# 	# protocol.agraph.layout = 'dot'
# 	# svg_data = protocol.agraph.draw(format='svg')


# 	# GET THE PLOT
# 	#svg_data = generate_some_svg_data()

# 	# RETURN THE PLOT
# 	# return HttpResponse(svg_data, mimetype="image/svg+xml")
# 	# return HttpResponse(svg_data, mimetype="image/png")


	
# 	A=P.AGraph() # init empty graph
# 	# set some default node attributes
# 	# A.node_attr['style']='filled'
# 	# A.node_attr['shape']='circle'
# 	# Add edges (and nodes)
# 	# A.add_edge(1,2)
# 	# A.add_edge(2,3)
# 	# A.add_edge(1,3)
# 	# layout with default (neato)
# 	svg_data = protocol.get_graph(A)

# 	png=svg_data.draw(format='svg') # draw png
# 	return HttpResponse(png, mimetype='image/svg+xml')



