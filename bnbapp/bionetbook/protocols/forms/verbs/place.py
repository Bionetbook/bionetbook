from protocols.forms import forms


class PlaceForm(forms.VerbForm):

    name = "Place"
    slug = "place"
    has_manual = True
    layers = ['item_to_place','target','conditional_statement','technique_comment','duration','duration_units']
    
    item_to_place = forms.CharField(required=False, help_text='what are you placing')
    target = forms.CharField(required=False, help_text='where are you placing it')
    conditional_statement = forms.CharField(required=False)
'''
place tubes on ice
Place a QIAquick spin column in a provided 2 ml collection tube
Place a QIAquick spin column in a provided 1.5 ml collection tube



'''