from protocols import forms


class CloseForm(forms.VerbForm):

    name = "Close"
    slug = "close"

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
