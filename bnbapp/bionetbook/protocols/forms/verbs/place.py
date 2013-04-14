from protocols.forms import forms


class PlaceForm(forms.VerbForm):

    name = "Place"
    slug = "place"

    add_conditional_statement = forms.CharField()
