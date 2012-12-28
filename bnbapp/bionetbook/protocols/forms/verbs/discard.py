from protocols.forms import forms


class DiscardForm(forms.VerbForm):

    name = "Discard"
    slug = "discard"

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
    describe_where = forms.CharField()
    edit_remarks = forms.CharField()
    edit_why_step = forms.CharField()
