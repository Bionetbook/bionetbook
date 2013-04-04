from protocols.forms import forms


class ExciseForm(forms.VerbForm):

    name = "Excise"
    slug = "excise"

    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    using_what = forms.CharField(required = False, help_text = 'rotator, shaker, manual etc')
    remarks = forms.CharField(required = False)
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    # edit_kit_name = forms.CharField()
    # edit_protocol_output = forms.CharField()
