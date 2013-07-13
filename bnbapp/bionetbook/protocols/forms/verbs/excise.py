from protocols.forms import forms


class ExciseForm(forms.VerbForm):

    name = "Excise"
    slug = "excise"
    has_manual = True
    layers = ['item_to_act','target','using_what','settify']

    item_to_act = forms.CharField(label='what are you exising')
    target = forms.CharField(required=False, help_text='where are you exising into')
    using_what = forms.CharField(required = False, help_text = 'rotator, shaker, manual etc')
    
    
