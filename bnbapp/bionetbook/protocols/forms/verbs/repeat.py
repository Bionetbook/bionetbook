from protocols.forms import forms


class RepeatForm(forms.VerbForm):

    name = "Repeat"
    slug = "repeat"
    has_manual = True
    layer=['item_to_act', 'number_of_times','conditonal_stetement' 'settify']

    item_to_act = forms.CharField(required=False, help_text='from what step are you repeating?', label='item to repeat')
    number_of_times = forms.IntegerField(required = False)
    conditional_statement = forms.CharField(required=False)
