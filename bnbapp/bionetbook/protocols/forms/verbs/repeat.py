from protocols.forms import forms


class RepeatForm(forms.VerbForm):

    name = "Repeat"
    slug = "repeat"
    has_manual = True
    layer=[]

    item_to_repeat = forms.CharField(required=False, help_text='from what step are you repeating?', label='item to repeat')
    
