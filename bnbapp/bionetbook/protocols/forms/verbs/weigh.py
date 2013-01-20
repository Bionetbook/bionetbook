from protocols.forms import forms


class WeighForm(forms.VerbForm):

    name = "Weigh"
    slug = "weigh"
    has_machines = True

    edit_what_remark = forms.CharField()
    edit_vessel_type = forms.CharField()
    duration_min_time = forms.IntegerField()
    describe_where = forms.CharField()
    edit_remarks = forms.CharField()
    specify_machine = forms.CharField()
    edit_why_step = forms.CharField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
