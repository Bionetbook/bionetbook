from protocols.forms import forms


class SonicateForm(forms.VerbForm):

    name = "Sonicate"
    slug = "sonicate"
    has_machine = True

    other_settings = forms.CharField(required = False)
    remarks = forms.CharField(required = False, initial = 'open or closed container, etc')
	
    