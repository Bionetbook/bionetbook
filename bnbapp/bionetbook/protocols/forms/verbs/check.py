from protocols.forms import forms


class CheckForm(forms.VerbForm):

    name = "Check"
    slug = "check"

    edit_what_remark = forms.CharField()
    specify_machine = forms.CharField()
    edit_remarks = forms.CharField()
    duration_min_time = forms.IntegerField()
    edit_protocol_output = forms.CharField()
    specify_tool = forms.CharField()
