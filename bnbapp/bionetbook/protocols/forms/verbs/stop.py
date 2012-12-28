from verbs.baseforms import forms


class StopForm(forms.VerbForm):

    name = "Stop"
    slug = "stop"

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
    specify_tool = forms.CharField()
    edit_kit_name = forms.CharField()
    edit_protocol_output = forms.CharField()
    edit_remarks = forms.CharField()
    edit_vessel_type = forms.CharField()
    describe_where = forms.CharField()
