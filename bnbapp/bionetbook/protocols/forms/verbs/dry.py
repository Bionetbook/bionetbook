from protocols.forms import forms


class DryForm(forms.VerbForm):

    name = "Dry"
    slug = "dry"
    has_manual = True
    layers = ['item_to_act', 'conditional_statement' , 'settify']
    

    item_to_act = forms.CharField(required=False, label='item to dry')
    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    