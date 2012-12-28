from protocols.forms import forms


class IncubateForm(forms.VerbForm):

    name = "Incubate"
    slug = "incubate"

    edit_what_remark = forms.CharField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    duration_min_time = forms.IntegerField()
    comment_why = forms.CharField()
    edit_remarks = forms.CharField()
    edit_input = forms.CharField()
    edit_protocol_output = forms.CharField()
    edit_vessel_type = forms.CharField()
    edit_kit_name = forms.CharField()
