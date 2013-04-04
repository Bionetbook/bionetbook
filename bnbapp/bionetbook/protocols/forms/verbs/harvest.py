from protocols.forms import forms


class HarvestForm(forms.VerbForm):

    name = "Harvest"
    slug = "harvest"

    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    remarks = forms.CharField(required = False)	
