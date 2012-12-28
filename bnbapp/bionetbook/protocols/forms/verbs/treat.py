from protocols.forms import forms


class TreatForm(forms.VerbForm):

    name = "Treat"
    slug = "treat"

    edit_what_remark = forms.CharField()
    edit_machine_settings = forms.CharField()
    duration_min_time = forms.IntegerField()
