from protocols.forms import forms


class DryForm(forms.VerbForm):

    name = "Dry"
    slug = "dry"
    has_manual = True
    layers = ['item_to_act', 'settify, technique_comment', 'conditional_statement']
    

    item_to_act = forms.CharField(required=False, label='item to aliquot')
    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    