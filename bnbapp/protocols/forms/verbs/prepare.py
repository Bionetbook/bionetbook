from protocols.forms import forms


class PrepareForm(forms.VerbForm):

    name = "Prepare"
    slug = "prepare"
    has_component = True

    item_to_prepare = forms.CharField()
    
