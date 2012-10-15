from verbs.baseforms import forms


class CloseForm(forms.VerbForm):

    name = "close"
    slug = "close"


    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()