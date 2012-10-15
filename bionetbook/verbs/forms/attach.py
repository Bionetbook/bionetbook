from verbs.baseforms import forms


class AttachForm(forms.VerbForm):

    name = "attach"
    slug = "attach"


    edit_what_remark = forms.CharField()
    describe_where = forms.CharField()
    duration_min_time = forms.IntegerField()