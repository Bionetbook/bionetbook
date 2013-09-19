from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib import messages
from protocols.models import Protocol
from django.core.exceptions import PermissionDenied
from django.http import Http404

# class ConfirmProfile(object):

#     def process_response(self, request, response):

#         my_profile = getattr(request, "my_profile", None)

#         if not hasattr(request, "user"):
#             return response

#         if request.user.is_anonymous():
#             return response

#         if my_profile == None:
#             current_path = request.get_full_path()

#             # TODO write this cleaner
#             paths = ('profile_update', 'logout', )
#             valid_path = False
#             for path in paths:
#                 if current_path.startswith(reverse(path)):
#                     valid_path = True
#             if not valid_path:
#                 messages.add_message(request, messages.ERROR, "Please fill out your profile.")
#                 return HttpResponseRedirect(reverse('profile_update'))

#         return response



class ProtocolAccess(object):

    def process_view(self, request, view_func, view_args, view_kwargs):

        if "protocol_slug" in view_kwargs:
            user = getattr(request, "user", None)

            if user:
                try:
                    protocol = Protocol.objects.get(slug=view_kwargs["protocol_slug"])
                except Protocol.DoesNotExist:
                    raise PermissionDenied

                if not protocol.user_has_access(user):
                    raise PermissionDenied   # How about returning a 404 response

        return

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     __traceback_hide__ = True
    #     toolbar = self.__class__.debug_toolbars.get(threading.currentThread().ident)
    #     if not toolbar:
    #         return
    #     result = None
    #     for panel in toolbar.panels:
    #         response = panel.process_view(request, view_func, view_args, view_kwargs)
    #         if response:
    #             result = response
    #     return result
