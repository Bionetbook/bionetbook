from protocols.forms import forms
from django.db.models.query import EmptyQuerySet
from django.utils.translation import ugettext_lazy as _

class CallForProtocolForm(forms.VerbForm):

    name = "Call For Protocol"
    slug = "call-for-protocol"
    has_manual = True
    layers = ['item_to_act', 'input_to_track', 'output_to_track']

    # protocol_name = forms.CharField(required = False, help_text='kit or protocol name')
    protocol_id = forms.ModelChoiceField(required=False, queryset=EmptyQuerySet(), label=_("Protocol"))
    # protocol_id = forms.ChoiceField(required=False, help_text='Select a protocol to link to', choices=[])
    input_to_track = forms.CharField(help_text = 'reagent, sample, molecule, compounds, strain etc.')
    input_notes = forms.CharField(required = False, help_text = 'concentration, volume, mass etc')
    output_to_track = forms.CharField(help_text = 'reagent, sample, molecule, compounds, strain etc.')
    output_notes = forms.CharField(required = False, help_text = 'concentration, volume, mass etc')
    # settings like concentration, volume, yield etc. 
    # remarks = forms.CharField(required = False)
    