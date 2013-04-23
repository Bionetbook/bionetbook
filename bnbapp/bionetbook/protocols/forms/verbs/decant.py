from protocols.forms import forms


class DecantForm(forms.VerbForm):

    name = "Decant"
    slug = "decant"
    has_manual = True
    layer= []
    
    item_to_act = forms.CharField(required=False, label='item to decant')
    target = forms.CharField(required=False, help_text='where are you placing it')