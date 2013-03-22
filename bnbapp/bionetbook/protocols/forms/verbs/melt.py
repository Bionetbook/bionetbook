from protocols.forms import forms


class MeltForm(forms.VerbForm):

    name = "Melt"
    slug = "melt"
    has_machine = True

    edit_what_remark = forms.CharField()
    specify_machine = forms.CharField()
    duration_min_time = forms.IntegerField()
