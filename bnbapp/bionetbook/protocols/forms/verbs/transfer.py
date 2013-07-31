from protocols.forms import forms
from core.utils import  VOLUME_UNITS, TIME_UNITS

class TransferForm(forms.VerbForm):

    name = "Transfer"
    slug = "transfer"
    has_manual = True
    layers = ['item_to_act','old_vessel','new_vessel','item_to_discard','settify']
    
    
    old_vessel = forms.CharField(required=False, help_text = 'Where are you transferring from?')
    new_vessel = forms.CharField(required=False, help_text = 'Where are you transferring to?')
    item_to_act = forms.CharField(required=False,help_text = 'what are you transferring?', label='item to transfer')
    item_to_discard = forms.CharField(required=False,help_text = 'careful not to transfer this part')
    min_vol = forms.FloatField(required=False)
    max_vol = forms.FloatField(required=False)
    vol_units = forms.ChoiceField(required=False, choices=VOLUME_UNITS )
    vol_comment = forms.CharField(required=False)
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds' )
    time_comment = forms.CharField(required=False)

'''
Transfer the transparent liquid above the lipid layer (middle of tube) to a fresh tube to separate RNA from DNA
Transfer the suspension to a new microcentrifuge tube. Be careful not to move the sand

'''