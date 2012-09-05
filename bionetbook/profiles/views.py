from django.views.generic import UpdateView

from braces.views import LoginRequiredMixin

from profiles.forms import ProfileForm
from profiles.models import Profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = Profile
    form_class = ProfileForm

    def get_object(self):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )
        return profile
