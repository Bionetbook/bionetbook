from verbs.baseforms import forms


class AddForm(forms.VerbForm):

    name = "add" # cannot silence the name without an error, the name here is redundant
    slug = "add"


    duration_min_time = forms.IntegerField()
    describe_where = forms.CharField()
    edit_remarks = forms.CharField()