from protocols.forms import forms


class DryForm(forms.VerbForm):

    name = "Dissolve"
    slug = "dissolve"
    has_component = True
    
    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    using_what = forms.CharField(required = False, help_text = 'rotator, shaker, manual etc')
    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')

