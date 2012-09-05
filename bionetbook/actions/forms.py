import floppyforms as forms

from actions.models import Action


class ActionForm(forms.ModelForm):

    class Meta:
        model = Action
        exclude = ('step', 'slug', 'verb_attributes', 'duration_in_seconds')
