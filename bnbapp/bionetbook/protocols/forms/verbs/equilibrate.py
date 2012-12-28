from protocols.forms import forms


class EquilibrateForm(forms.VerbForm):

    name = "Equilibrate"
    slug = "equilibrate"

    edit_what_remark = forms.CharField()
    add_with_what = forms.CharField()
    duration_min_time = forms.IntegerField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    edit_what_to = forms.CharField()
