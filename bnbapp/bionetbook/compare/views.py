from django.http import HttpResponse
from compare.models import ProtocolPlot



def protocol_plot(request, protocol_slug):

	svg_plot = None
	# GET THE PROTOCOL
	protocol = ProtocolPlot.objects.get(name__incontains=protocol_slug)
	protocol.agraph.layout = 'dot'
	svg_data = protocol.agraph.draw(format='svg')


	# GET THE PLOT
    #svg_data = generate_some_svg_data()

    # RETURN THE PLOT
    return HttpResponse(svg_data, mimetype="image/svg+xml")
