from protocols.forms import verbs as verb_forms
from protocols import forms


def get_verb_list():
    verb_list = []
    for attr_name in dir(verb_forms):
        form_candidate = getattr(verb_forms, attr_name, None)
        try:
            if issubclass(form_candidate, forms.Form):
                verb_list.append(form_candidate)
        except TypeError:
            continue
    return verb_list

VERB_LIST = get_verb_list()
VERB_CHOICES = [(x.slug, x.name) for x in VERB_LIST]
