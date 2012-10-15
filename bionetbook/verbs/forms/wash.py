from verbs.baseforms import forms


class WashForm(forms.VerbForm):

    name = "wash"
    slug = "wash"


    edit_what_remark = forms.CharField()
    add_with_what = forms.CharField()
    duration_min_time = forms.IntegerField()