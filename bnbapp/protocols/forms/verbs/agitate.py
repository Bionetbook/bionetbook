from protocols.forms import forms


class AgitateForm(forms.VerbForm):

    name = "Agitate"
    slug = "agitate"
    has_machine = True

    # item_to_place = forms.CharField(required=False, help_text='what are you placing')
    # conditional_statement = forms.CharField(required = False, help_text = 'If X, do Y')
    
