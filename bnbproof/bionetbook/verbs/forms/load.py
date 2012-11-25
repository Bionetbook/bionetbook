from verbs.baseforms import forms


class LoadForm(forms.VerbForm):

    name = "load"
    slug = "load"


    describe_where = forms.CharField()
    duration_min_time = forms.IntegerField()
    edit_what_remark = forms.CharField()