from protocols.forms import forms


class PourOffForm(forms.VerbForm):

    name = "Pour Off"
    slug = "pour-off"

    duration_in_seconds = forms.IntegerField()
    edit_what_remark = forms.CharField()
