from django.views.generic import ListView, DetailView, CreateView, UpdateView

from protocols.forms import ProtocolForm
from protocols.models import Protocol


class ProtocolDetailView(DetailView):

    model = Protocol


class ProtocolListView(ListView):

    model = Protocol


class ProtocolCreateView(CreateView):

    model = Protocol
    form_class = ProtocolForm
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ProtocolCreateView, self).form_valid(form)
        
    def get_success_url(self):
        
        return self.object.get_absolute_url()
        
class ProtocolUpdateView(UpdateView):
    
    model = Protocol
    form_class = ProtocolForm