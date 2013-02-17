from protocols.forms import forms



class AddForm(forms.VerbForm):

    name = "Add"  # cannot silence the name without an error, the name here is redundant
    slug = "add"
    has_components = True

    duration_min_time = forms.IntegerField(help_text='this is the minimal time this should take')
    describe_where = forms.CharField()
    edit_remarks = forms.CharField()
    add_what = forms.CharField()
