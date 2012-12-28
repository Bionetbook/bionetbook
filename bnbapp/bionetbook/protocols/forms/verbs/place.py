from protocols.forms import forms


class PlaceForm(forms.VerbForm):

    name = "Place"
    slug = "place"

    edit_what_remark = forms.CharField()
    describe_where = forms.CharField()
    duration_min_time = forms.IntegerField()
    add_conditional_statement = forms.CharField()
