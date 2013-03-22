from protocols.forms import forms


class AdjustForm(forms.VerbForm):

    name = "Adjust"
    slug = "adjust"
    has_machine = True

    # duration = forms.IntegerField(help_text='this is the minimal time this should take')
    edit_what_to = forms.CharField(required = False, help_text = 'what are you adjusting')
    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    # specify_machine = forms.CharField(required = False, help_text = 'het block, incubator etc')
    
