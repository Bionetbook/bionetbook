from django.http import Http404
from django.views.generic import TemplateView


class DashboardView(TemplateView):

    template_name = "core/dashboard.html"
