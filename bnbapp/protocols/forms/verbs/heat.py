from protocols.forms import forms


class HeatForm(forms.VerbForm):

    name = "Heat"
    slug = "heat"
    has_machine = True

    other_settings = forms.CharField(required = False)
    remarks = forms.CharField(required = False, initial = 'open or closed container, etc')
	
    