from protocols.forms import verbs as verb_forms
from protocols.forms import forms

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
VERB_FORM_DICT = {x.slug: x for x in VERB_LIST}

MACHINE_VERBS = [x.slug for x in VERB_LIST if x.has_machine]
COMPONENT_VERBS = [x.slug for x in VERB_LIST if x.has_component]
THERMOCYCLER_VERBS = [x.slug for x in VERB_LIST if x.has_thermocycler]

print [x.name for x in VERB_LIST]