from protocols.forms import forms


class DrainForm(forms.VerbForm):

    name = "Drain"
    slug = "drain"

    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')


    remarks = forms.CharField(required = False)

