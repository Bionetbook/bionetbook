from verbs.baseforms import forms


class GrindForm(forms.VerbForm):

    name = "Grind"
    slug = "grind"

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
