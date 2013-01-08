from django.views.generic import FormView
from django.views.generic.edit import ModelFormMixin, CreateView

from interest.models import Interest
from interest.forms import InterestForm

# Create your views here.
class InterestCreate(CreateView):
    #template_name = 'interest/interest_create_view.html'
    #form_class = InterestForm
    success_url = '/'
    model = Interest

    #def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
    #    form.send_email()
    #    return super(ContactView, self).form_valid(form)

