from protocols.forms import forms


class HeatForm(forms.VerbForm):

    name = "heat"
    slug = "heat"
    has_machines = True

    
    edit_what_remark = forms.CharField(required = False, help_text='sample name, default is tube')
    # machine = forms.CharField(required = False, help_text='enter machine name')
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    duration_min_time = forms.IntegerField()
    # other_settings = forms.CharField(required = False)
    edit_remarks = forms.CharField(required = False)
	
    