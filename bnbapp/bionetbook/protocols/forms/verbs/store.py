from protocols.forms import forms


class StoreForm(forms.VerbForm):

    name = "Store"
    slug = "store"

    min_temp = forms.IntegerField(required=False)
    max_temp = forms.IntegerField()
    duration = forms.IntegerField(help_text='how long can it stay on ice?', required = False)
   
