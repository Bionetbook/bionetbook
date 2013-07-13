from protocols.forms import forms


class DiscardForm(forms.VerbForm):

    name = "Discard"
    slug = "discard"
    has_manual = True
    layers = ['item_to_act','item_to_retain','conditional_statement','settify']

    item_to_act = forms.CharField(required=False, label='item to discard')
    item_to_retain = forms.CharField()
    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    remarks = forms.CharField(required = False)
