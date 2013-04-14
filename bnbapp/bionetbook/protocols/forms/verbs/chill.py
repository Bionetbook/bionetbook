from protocols.forms import forms


class ChillForm(forms.VerbForm):

    name = "Chill"
    slug = "chill"
    has_machine = True

    # duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    remarks = forms.CharField(required = False)
  