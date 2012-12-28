from protocols.forms import forms


class GrowForm(forms.VerbForm):

    name = "Grow"
    slug = "grow"

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
    edit_what_to = forms.CharField()
    edit_vessel_type = forms.CharField()
    edit_remarks = forms.CharField()
    describe_where = forms.CharField()
    specify_date = forms.DateField()
    comment_why = forms.CharField()
