from protocols.forms import forms


class CheckForm(forms.VerbForm):

    name = "Check"
    slug = "check"

    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    specify_tool = forms.CharField(required = False, help_text = 'calculator, scissors, pippete, blade etc')
    remarks = forms.CharField(required = False)
   
    
    
