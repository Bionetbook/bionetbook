from protocols.forms import forms


class EluteForm(forms.VerbForm):

    name = "Elute"
    slug = "elute"

    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    using_what = forms.CharField(required = False, help_text = 'rotator, shaker, manual etc')
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    remarks = forms.CharField(required = False)
