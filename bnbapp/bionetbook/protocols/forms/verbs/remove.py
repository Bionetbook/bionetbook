from protocols.forms import forms


class RemoveForm(forms.VerbForm):

    name = "Remove"
    slug = "remove"
    has_manual = True
    layers = ['item_to_act','target','specify_tool','conditional_statement','settify']

    item_to_act = forms.CharField(required=False, help_text='what are you removing', label='item to remove')
    target = forms.CharField(required=False, help_text='where are you placing it')
    conditional_statement = forms.CharField(required=False)
    specify_tool = forms.CharField(required=False)
    
