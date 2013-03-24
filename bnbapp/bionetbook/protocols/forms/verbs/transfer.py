from protocols.forms import forms
VOLUME_UNITS = (("l","liter"),("ml","Mililiter"), ("ul","microliter"), )

class TransferForm(forms.VerbForm):

    name = "Transfer"
    slug = "transfer"

    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    old_vessel = forms.CharField(help_text = 'Where are you transferring from?')
    new_vessel = forms.CharField(help_text = 'Where are you transferring to?')
    target = forms.CharField(help_text = 'what are you transferring?')
    volume = forms.FloatField()
    volume_units = forms.ChoiceField(choices = VOLUME_UNITS)
