from protocols.forms import forms


class PipetteOutForm(forms.VerbForm):

    name = "Pipette Out"
    slug = "pipette-out"

    what_to_pipette_out = forms.CharField()
