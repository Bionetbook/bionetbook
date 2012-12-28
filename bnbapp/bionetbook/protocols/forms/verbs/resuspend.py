from protocols.forms import forms


class ResuspendForm(forms.VerbForm):

    name = "Resuspend"
    slug = "resuspend"

    edit_what_remark = forms.CharField()
    add_with_what = forms.CharField()
    duration_min_time = forms.IntegerField()
    edit_protocol_output = forms.CharField()
    edit_remarks = forms.CharField()
