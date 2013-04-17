from protocols.forms import forms


class CallForProtocolForm(forms.VerbForm):

    name = "Call For Protocol"
    slug = "call-for-protocol"
    has_component = True

    protocol_type = forms.CharField(required = False, help_text = 'describe the basic chemistry')
    protocol_kit_name = forms.CharField(required = False, help_text = 'kit name')
    protocol_link = forms.CharField(required=False, help_text='enter the protocol URL, add both / at the beginning and end')
    input_to_track = forms.CharField(help_text = 'reagent, sample, molecule, compounds, strain etc.')
    input_notes = forms.CharField(required = False, help_text = 'concentration, volume, mass etc')
    output_to_track = forms.CharField(help_text = 'reagent, sample, molecule, compounds, strain etc.')
    output_notes = forms.CharField(required = False, help_text = 'concentration, volume, mass etc')
    # settings like concentration, volume, yield etc. 
    remarks = forms.CharField(required = False)
    