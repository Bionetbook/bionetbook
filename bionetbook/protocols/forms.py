import floppyforms as forms

from protocols.models import Protocol


class ProtocolForm(forms.ModelForm):

    class Meta:
        model = Protocol
        exclude = ('parent', 'owner', 'slug')
