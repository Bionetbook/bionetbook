from protocols.forms import forms


class ApplyForm(forms.VerbForm):

    name = "Apply"
    slug = "apply"
    has_manual = True
    layers = ['item_to_act', 'target', 'number_of_times','settify']

    # duration = forms.IntegerField(help_text='this is the minimal time this should take')
    # edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    item_to_act = forms.CharField(required=False, help_text='what are you applying', label='item to apply')
    target = forms.CharField(required=False, help_text='where are you placing it')
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    specify_tool = forms.CharField(required = False, help_text = 'not machine, scissors, pippete, blade etc')
    number_of_times = forms.IntegerField(required = False)
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds', initial = 'sec' )
    time_comment = forms.CharField(required=False)