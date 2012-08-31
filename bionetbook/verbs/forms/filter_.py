from verbs.baseforms import forms


class FilterForm(forms.VerbForm):

    name = "filter"
    slug = "filter"

    duration_in_seconds = forms.IntegerField()
