from verbs.baseforms import forms


class SwitchoffForm(forms.VerbForm):

    name = "Switchoff"
    slug = "Switchoff"


    edit_remarks = forms.CharField()
    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
    edit_why_step = forms.CharField()
    describe_where = forms.CharField()
    specify_machine = forms.CharField()