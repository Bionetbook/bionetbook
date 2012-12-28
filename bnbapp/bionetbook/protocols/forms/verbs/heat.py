from protocols.forms import forms


class HeatForm(forms.VerbForm):

    name = "heat"
    slug = "heat"


    edit_what_remark = forms.CharField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    duration_min_time = forms.IntegerField()
    edit_remarks = forms.CharField()