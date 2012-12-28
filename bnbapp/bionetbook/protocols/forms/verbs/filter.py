from protocols.forms import forms


class FilterForm(forms.VerbForm):

    name = "Filter"
    slug = "filter"

    comment_why = forms.CharField()
    duration_min_time = forms.IntegerField()
