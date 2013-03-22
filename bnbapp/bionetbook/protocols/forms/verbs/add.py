from protocols.forms import forms



class AddForm(forms.VerbForm):

    name = "Add"  # cannot silence the name without an error, the name here is redundant
    slug = "add"
    has_component = True

    duration = forms.IntegerField(help_text='this is the minimal time this should take')
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    remarks = forms.CharField(required = False)
    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
