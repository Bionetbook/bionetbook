from django.http import HttpResponse

import django.utils.simplejson as json

from protocols.models import Protocol

def protocol_detail(request, protocol_slug):
    if request.method == 'GET':
		p = Protocol.objects.get(slug=protocol_slug)
		return HttpResponse(json.dumps(p.data), mimetype="application/json")