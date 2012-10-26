from verbs.baseforms import forms


class VortexForm(forms.VerbForm):

    name = "Vortex"
    slug = "vortex"

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    comment_why = forms.CharField()
    describe_where = forms.CharField()
