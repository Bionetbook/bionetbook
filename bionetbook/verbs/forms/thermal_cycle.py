from verbs.baseforms import forms


class ThermalCycleForm(forms.VerbForm):

    name = "thermal cycle"
    slug = "thermal-cycle"

   
    min_temp=forms.IntegerField()
    max_temp=forms.IntegerField()
    duration_min_time=forms.IntegerField()
    edit_kit_name=forms.CharField()
    edit_protocol_output=forms.CharField()
    edit_remarks=forms.CharField()