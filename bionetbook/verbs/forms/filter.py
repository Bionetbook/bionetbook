from verbs.baseforms import forms


class FilterForm(forms.VerbForm):

    name = "filter"
    slug = "filter"


    comment_why = forms.CharField()
    duration_min_time = forms.IntegerField()