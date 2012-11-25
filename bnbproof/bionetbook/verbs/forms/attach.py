from verbs.baseforms import forms


class AttachForm(forms.VerbForm):

    name = "Attach"
    slug = "attach"

    edit_what_remark = forms.CharField()
    describe_where = forms.CharField()
    duration_min_time = forms.IntegerField()
