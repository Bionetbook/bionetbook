from protocols.models import Protocol

def validate_user(request, component, protocol_slug):
    if request.method == 'GET':
    	p = Protocol.objects.find(slug=protocol_slug)
		return HttpResponse(json.dumps(p.data), mimetype="application/json")