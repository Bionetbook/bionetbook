from verbs.baseforms import forms


class CutForm(forms.VerbForm):

    name = "cut"
    slug = "cut"


    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
    comment_why = forms.CharField()