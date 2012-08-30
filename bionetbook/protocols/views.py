from django.views.generic import ListView, DetailView, CreateView

from protocols.models import Protocol


class ProtocolDetailView(DetailView):

    model = Protocol


class ProtocolListView(ListView):

    model = Protocol


class ProtocolCreateView(CreateView):

    model = Protocol