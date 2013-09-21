from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib import messages
from protocols.models import Protocol
from django.http import Http404
from django.shortcuts import get_object_or_404


class ProtocolAccess(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.protocol = None
        request.protocols = []
        user = getattr(request, "user", None)   # GET THE USER OBJECT FROM THE REQUEST

        if "protocol_slug" in view_kwargs and user:
            request.protocol = self.get_protocol(user, view_kwargs['protocol_slug'])
            request.protocol_edit = request.protocol.user_can_edit(user)

        for key in ['protocol_a_slug', 'protocol_b_slug']:          # THIS IF FOR HANDLING A LIST OF PROTOCOLS.  PROBABLY SHOULD UPDATE THIS AT SOME POINT.
            if key in view_kwargs:
                request.protocols.append(user, view_kwargs[key])

        # return Protocol.objects.filter(id__in=self.data['protocols'])     # <- SHOULD USE SOMETHING MORE LIKE THIS

        return

    def get_protocol(self, user, slug):
        protocol = get_object_or_404( Protocol, slug=slug )

        if not protocol.user_has_access(user):
            print "%s has no access to %s" % (user, protocol)
            raise Http404()   # How about returning a 404 response

        return protocol
