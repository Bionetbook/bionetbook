from protocols.forms import forms


class ElectrophoreseForm(forms.VerbForm):

    name = "Electrophorese"
    slug = "electrophorese"
    has_machine = True

    edit_remarks = forms.CharField()
    duration_min_time = forms.IntegerField()
    specify_machine = forms.CharField()
    min_voltage = forms.IntegerField()
    max_voltage = forms.IntegerField()