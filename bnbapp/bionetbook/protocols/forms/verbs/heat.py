from protocols.forms import forms


class HeatForm(forms.VerbForm):

    name = "Heat"
    slug = "heat"
    has_machine = True

    
    sample_name = forms.CharField(required = False, help_text='sample name, default is tube')
    # min_temp = forms.IntegerField()
    # max_temp = forms.IntegerField()
    # duration_min_time = forms.IntegerField()
    other_settings = forms.CharField(required = False)
    remarks = forms.CharField(required = False, initial = 'open or closed container, etc')
	
    