from verbs.baseforms import forms


class DryForm(forms.VerbForm):

    name = "dissolve"
    slug = "dissolve"


    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()