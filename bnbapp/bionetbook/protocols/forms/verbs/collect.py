from protocols import forms


class CollectForm(forms.VerbForm):

    name = "Collect"
    slug = "collect"

    duration_in_seconds = forms.IntegerField()
