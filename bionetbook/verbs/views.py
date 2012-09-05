from django.http import Http404
from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin

from verbs import forms as verb_forms
from verbs.utils import VERB_LIST


class VerbBaseView(object):

    def get_verb_form(self, slug=None):

        if slug is None:
            slug = self.kwargs.get('slug')

        # convert the slug into a form name
        form_name = "".join([x.title() for x in slug.split('-')]) + "Form"

        form = getattr(verb_forms, form_name, None)

        if form is None:
            raise  Http404

        return form


class VerbDetailView(VerbBaseView, TemplateView):

    template_name = "verbs/verb_detail.html"

    def get_context_data(self, **kwargs):
        context = super(VerbDetailView, self).get_context_data(**kwargs)

        context["verb"] = self.get_verb_form()
        return context


class VerbListView(TemplateView):

    template_name = "verbs/verb_list.html"

    def get_context_data(self, **kwargs):
        context = super(VerbListView, self).get_context_data(**kwargs)
        context['verb_list'] = VERB_LIST
        return context
