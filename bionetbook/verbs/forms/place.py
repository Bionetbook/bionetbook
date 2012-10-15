from verbs.baseforms import forms


class PlaceForm(forms.VerbForm):

    name = "place"
    slug = "place"


    edit_what_remark = forms.CharField()
    describe_where = forms.CharField()
    duration_min_time = forms.IntegerField()
    add_conditional_statement = forms.CharField()