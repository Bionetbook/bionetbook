from verbs.baseforms import forms


class ExciseForm(forms.VerbForm):

    name = "Excise"
    slug = "excise"

    edit_what_remark = forms.CharField()
    specify_tool = forms.CharField()
    edit_remarks = forms.CharField()
    duration_min_time = forms.IntegerField()
    edit_kit_name = forms.CharField()
    edit_protocol_output = forms.CharField()
