from protocols import forms


class AddForm(forms.VerbForm):

    name = "Add"  # cannot silence the name without an error, the name here is redundant
    slug = "add"

    duration_min_time = forms.IntegerField()
    describe_where = forms.CharField()
    edit_remarks = forms.CharField()
    add_what = forms.CharField()
