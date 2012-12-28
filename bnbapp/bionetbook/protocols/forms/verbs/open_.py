from protocols.forms import forms


class OpenForm(forms.VerbForm):

    name = "Open"
    slug = "open"

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
    describe_where = forms.CharField()
