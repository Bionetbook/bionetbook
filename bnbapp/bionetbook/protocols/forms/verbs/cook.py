from protocols import forms


class CookForm(forms.VerbForm):

    name = "Cook"
    slug = "cook"

    duration_in_seconds = forms.IntegerField()
    temperature = forms.IntegerField()
