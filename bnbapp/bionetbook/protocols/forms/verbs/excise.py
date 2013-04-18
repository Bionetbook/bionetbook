from protocols.forms import forms


class ExciseForm(forms.VerbForm):

    name = "Excise"
    slug = "excise"
    has_manual = True
    layers = ['item_to_exise','target','using_what','duration','duration_units']

    item_to_exise = forms.CharField(help_text='what are you exising')
    target = forms.CharField(required=False, help_text='where are you exising into')
    using_what = forms.CharField(required = False, help_text = 'rotator, shaker, manual etc')
    remarks = forms.CharField(required = False)
    
