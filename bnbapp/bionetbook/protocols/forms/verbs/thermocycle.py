from protocols.forms import forms


class ThermocycleForm(forms.VerbForm):

    name = "Thermmocycle"
    slug = "thermocycle"
    has_thermocycler = True

    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    duration_min_time = forms.IntegerField()
    edit_kit_name = forms.CharField()
    edit_protocol_output = forms.CharField()
    edit_remarks = forms.CharField()
