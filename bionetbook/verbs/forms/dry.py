from verbs.baseforms import forms


class DryForm(forms.VerbForm):

    name = "dry"
    slug = "dry"


    duration_min_time = forms.IntegerField()
    edit_what_remark = forms.CharField()
    add_with_what = forms.CharField()