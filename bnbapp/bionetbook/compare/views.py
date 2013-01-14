from django.http import HttpResponse

def protocol_plot(request, protocol_slug):

	svg_plot = None
	# GET THE PROTOCOL

	# GET THE PLOT
    #svg_data = generate_some_svg_data()

    # RETURN THE PLOT
    return HttpResponse(svg_data, mimetype="image/svg+xml")
