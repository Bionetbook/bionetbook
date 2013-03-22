from protocols.forms import forms


class CallForProtocolForm(forms.VerbForm):

    name = "Call For Protocol"
    slug = "call-for-protocol"
    has_component = True

    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    protocol_type = forms.CharField(required = False, help_text = 'describe the basic chemistry')
    input_name = forms.CharField(help_text = 'reagent, sample, molecule, compouns, strain etc.')
    output_name = forms.CharField(help_text = 'reagent, sample, molecule, compouns, strain etc.')
    remarks = forms.CharField(required = False)
    comment_why = forms.CharField(required = False)