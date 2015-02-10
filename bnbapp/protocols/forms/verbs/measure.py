from protocols.forms import forms
from core.utils import CONCENTRATION_UNITS

class MeasureForm(forms.VerbForm):

    name = "Measure"
    slug = "measure"
    has_machine = True

    what_are_you_measuring = forms.CharField(help_text = 'RNA concentration')
    measurement_value = forms.FloatField(required = False)
    measurement_units = forms.ChoiceField(choices = CONCENTRATION_UNITS)
    device = forms.CharField(required = False, help_text ='nanostring, mass_spec, scale etc')
    file_of_measurement = forms.FileField(required = False)

