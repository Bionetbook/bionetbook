from protocols.forms import forms


class DiscardForm(forms.VerbForm):

    name = "Discard"
    slug = "discard"
    has_manual = True
    layers = ['item_to_discard','item_to_retain','conditional_statement','technique_comment','duration','duration_units']

    item_to_discard = forms.CharField()
    item_to_retain = forms.CharField()
    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    remarks = forms.CharField(required = False)
