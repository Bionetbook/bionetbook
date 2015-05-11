from protocols.forms import forms
from core.utils import TIME_UNITS

class ElectrophoreseForm(forms.VerbForm):

    name = "Electrophorese"
    slug = "electrophorese"
    has_machine = True

    model = forms.CharField(required = False, label='machine_model')
    min_voltage = forms.IntegerField(required = False)
    max_voltage = forms.IntegerField(required = False)
    voltage_units = forms.CharField(initial ='volts')