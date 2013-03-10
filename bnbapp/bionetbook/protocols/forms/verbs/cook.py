from protocols.forms import forms


class CookForm(forms.VerbForm):

    name = "Cook"
    slug = "cook"
    has_machine = True

    duration_in_seconds = forms.IntegerField()
    temperature = forms.IntegerField()
