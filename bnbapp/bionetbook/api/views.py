from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

import django.utils.simplejson as json

from protocols.models import Protocol

def protocol_detail(request, protocol_slug):
    if request.method == 'GET':
        try:
            p = Protocol.objects.get(slug=protocol_slug)
            return HttpResponse(json.dumps(p.data), mimetype="application/json")
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'error':'ObjectDoesNotExist', 'description':'Could not find the requested protocol.'}), mimetype="application/json")
