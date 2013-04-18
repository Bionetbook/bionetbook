from protocols.forms import forms


class CheckForm(forms.VerbForm):

    name = "Check"
    slug = "check"
    has_machine = True

    item_to_check = forms.CharField(help_text='what are you checking')
    target = forms.CharField(required=False, help_text='criteria for checking, for example 15 ng/ul')
    unit_comment = forms.CharField(required=False)
    remarks = forms.CharField(required = False)
   
    
    
