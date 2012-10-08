from verbs.baseforms import forms


class PipetteoutForm(forms.VerbForm):

    name = "Pipetteout"
    slug = "Pipetteout"


    Edit_what_remark=forms.CharField()
    Edit_remarks=forms.CharField()
    Duration_Min_Time=forms.IntegerField()