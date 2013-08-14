from protocols.forms import forms
from django.db.models.query import EmptyQuerySet
# from protocols.models import Protocol


class CallForProtocolForm(forms.VerbForm):

    name = "Call For Protocol"
    slug = "call-for-protocol"
    has_component = True

    protocol_name = forms.CharField(required = False, help_text = 'kit or protocol name')
    protocol_link = forms.ModelChoiceField(required=False, queryset=EmptyQuerySet())
    # protocol_id = forms.ChoiceField(required=False, help_text='Select a protocol to link to', choices=[])
    input_to_track = forms.CharField(help_text = 'reagent, sample, molecule, compounds, strain etc.')
    input_notes = forms.CharField(required = False, help_text = 'concentration, volume, mass etc')
    output_to_track = forms.CharField(help_text = 'reagent, sample, molecule, compounds, strain etc.')
    output_notes = forms.CharField(required = False, help_text = 'concentration, volume, mass etc')
    # settings like concentration, volume, yield etc. 
    # remarks = forms.CharField(required = False)
    