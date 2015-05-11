from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages


class ConfirmProfile(object):

    def process_response(self, request, response):

        my_profile = getattr(request, "my_profile", None)

        if not hasattr(request, "user"):
            return response

        if request.user.is_anonymous():
            return response

        if my_profile == None:
            current_path = request.get_full_path()

            # TODO write this cleaner
            paths = ('profile_update', 'logout', )
            valid_path = False
            for path in paths:
                if current_path.startswith(reverse(path)):
                    valid_path = True
            if not valid_path:
                messages.add_message(request, messages.ERROR, "Please fill out your profile.")
                return HttpResponseRedirect(reverse('profile_update'))

        return response
