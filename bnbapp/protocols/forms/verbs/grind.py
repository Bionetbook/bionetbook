from protocols.forms import forms


class GrindForm(forms.VerbForm):

    name = "Grind"
    slug = "grind"
    has_machine = True

    remarks = forms.CharField(required = False)
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    specify_tool = forms.CharField(required = False, help_text = 'not machine, scissors, pippete, blade etc')
    
