from protocols.forms import forms


class WashForm(forms.VerbForm):

    name = "Wash"
    slug = "wash"
    has_component = True

    item_to_act = forms.CharField(required=False, help_text='what are you washing', label='item to wash')
    number_of_times = forms.IntegerField(initial='1')
