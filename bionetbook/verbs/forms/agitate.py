from verbs.baseforms import forms


class AgitateForm(forms.VerbForm):

    name = "agitate"
    slug = "agitate"

    duration_in_seconds = forms.IntegerField()
