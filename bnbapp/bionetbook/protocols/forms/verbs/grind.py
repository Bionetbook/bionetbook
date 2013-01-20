from protocols.forms import forms


class GrindForm(forms.VerbForm):

    name = "Grind"
    slug = "grind"
    has_machines = True

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
