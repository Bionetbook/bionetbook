from protocols.forms import forms


class AliquotForm(forms.VerbForm):

    name = "Aliquot"
    slug = "aliquot"

    edit_what_remark = forms.CharField()
    edit_vessel_type = forms.CharField()
    duration_min_time = forms.IntegerField()
