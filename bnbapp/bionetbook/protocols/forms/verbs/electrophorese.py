from protocols.forms import forms


class ElectrophoreseForm(forms.VerbForm):

    name = "Electrophorese"
    slug = "electrophorese"
    has_machine = True

    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    specify_machine = forms.CharField()
    min_voltage = forms.IntegerField()
    max_voltage = forms.IntegerField()
    remarks = forms.CharField(required = False)