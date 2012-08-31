from verbs.baseforms import forms


class AttachForm(forms.VerbForm):

    name = "attach"
    slug = "attach"

    duration_in_seconds = forms.IntegerField()
