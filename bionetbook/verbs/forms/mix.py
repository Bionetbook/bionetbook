from verbs.baseforms import forms


class MixForm(forms.VerbForm):

    name = "mix"
    slug = "mix"


    duration_min_time = forms.IntegerField()
    comment_why = forms.CharField()
    edit_remarks = forms.CharField()