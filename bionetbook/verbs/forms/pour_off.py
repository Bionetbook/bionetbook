from verbs.baseforms import forms


class PourOffForm(forms.VerbForm):

    name = "pour off"
    slug = "pour-off"

    duration_in_seconds = forms.IntegerField()
    edit_what_remark=forms.CharField()
    