from protocols import forms


class PipetteOutForm(forms.VerbForm):

    name = "Pipette Out"
    slug = "pipette-out"

    duration_in_seconds = forms.IntegerField()
    edit_what_remark = forms.CharField()
    edit_remarks = forms.CharField()
