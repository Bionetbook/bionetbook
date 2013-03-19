from protocols.forms import forms


class ThermocycleForm(forms.VerbForm):

    name = "Thermmocycle"
    slug = "thermocycle"
    has_thermocycler = True

    phase_name = forms.CharField(required = False, initial = 'Initiaion denaturation')
    min_temp = forms.FloatField()
    max_temp = forms.FloatField(required = False)
    min_time = forms.FloatField()
    max_time = forms.FloatField(required = False)
    cycles = forms.IntegerField(required = False)
    cycle_back_to = forms.ChoiceField(required = False, choices = (('1', 'first'),('2', 'second'),('3', 'third'),('4', 'fourth'),('5', 'fifth')))
