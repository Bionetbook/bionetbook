from verbs.baseforms import forms


class SwitchOffForm(forms.VerbForm):

    name = "switch off"
    slug = "switch-off"

    duration_in_seconds = forms.IntegerField()
    edit_remarks = forms.CharField()
    edit_what_remark = forms.CharField()
    edit_why_step = forms.CharField()
    describe_where = forms.CharField()
    specify_machine = forms.CharField()