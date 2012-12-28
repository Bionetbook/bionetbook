from protocols import forms


class EluteForm(forms.VerbForm):

    name = "Elute"
    slug = "elute"

    edit_what_remark = forms.CharField()
    edit_into = forms.CharField()
    add_with_what = forms.CharField()
    duration_min_time = forms.IntegerField()
    edit_remarks = forms.CharField()
