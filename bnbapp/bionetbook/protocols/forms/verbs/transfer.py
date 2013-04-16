from protocols.forms import forms
VOLUME_UNITS = (("l","liter"),("ml","Mililiter"), ("ul","microliter"), )

class TransferForm(forms.VerbForm):

    name = "Transfer"
    slug = "transfer"
    has_manual = True
    
    old_vessel = forms.CharField(help_text = 'Where are you transferring from?')
    new_vessel = forms.CharField(help_text = 'Where are you transferring to?')
    item_to_place = forms.CharField(help_text = 'what are you transferring?')
    item_to_discard = forms.CharField(help_text = 'careful not to transfer this part')
    min_vol = forms.FloatField()
    vol_units = forms.ChoiceField(choices = VOLUME_UNITS)
    


'''
Transfer the transparent liquid above the lipid layer (middle of tube) to a fresh tube to separate RNA from DNA
Transfer the suspension to a new microcentrifuge tube. Be careful not to move the sand

'''