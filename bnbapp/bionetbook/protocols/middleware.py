from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib import messages
from protocols.models import Protocol
from django.http import Http404


class ProtocolAccess(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.protocol = None

        if "protocol_slug" in view_kwargs:
            user = getattr(request, "user", None)   # GET THE USER OBJECT FROM THE REQUEST

            if user:
                try:
                    request.protocol = Protocol.objects.get(slug=view_kwargs["protocol_slug"])
                except Protocol.DoesNotExist:
                    print "%s failed to access non-existant protocol" % (user)
                    raise Http404()

                if not request.protocol.user_has_access(user):
                    print "%s failed to access %s" % (user, request.protocol)
                    raise Http404()   # How about returning a 404 response

        return
