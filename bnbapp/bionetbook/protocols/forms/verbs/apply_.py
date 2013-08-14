from protocols.forms import forms


class ApplyForm(forms.VerbForm):

    name = "Apply"
    slug = "apply"

    # duration = forms.IntegerField(help_text='this is the minimal time this should take')
    # edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    item_to_act = forms.CharField(required=False, help_text='what are you applying', label='item to apply')
    target = forms.CharField(required=False, help_text='where are you placing it')
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    specify_tool = forms.CharField(required = False, help_text = 'not machine, scissors, pippete, blade etc')
    number_of_times = forms.IntegerField(required = False)