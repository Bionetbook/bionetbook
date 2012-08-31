from django.http import Http404
from django.views.generic import TemplateView

from verbs import forms as verb_forms
from verbs.baseforms import forms


class VerbDetailView(TemplateView):

    template_name = "verbs/verb_detail.html"

    def get_context_data(self, **kwargs):
        context = super(VerbDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug')

        # convert the slug into a form name
        form_name = "".join([x.title() for x in slug.split('-')]) + "Form"

        form = getattr(verb_forms, form_name, None)

        if form is None:
            raise  Http404

        context["verb"] = form
        return context


class VerbListView(TemplateView):

    template_name = "verbs/verb_list.html"

    def get_context_data(self, **kwargs):
        context = super(VerbListView, self).get_context_data(**kwargs)
        verb_list = []
        for attr_name in dir(verb_forms):
            form_candidate = getattr(verb_forms, attr_name, None)
            try:
                if issubclass(form_candidate, forms.Form):
                    verb_list.append(form_candidate)
            except TypeError:
                continue

        context['verb_list'] = verb_list
        return context
