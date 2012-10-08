from verbs.baseforms import forms


class AliquotForm(forms.VerbForm):

    name = "aliquot"
    slug = "aliquot"


    Edit_what_remark=forms.CharField()
    Edit_vessel_type=forms.CharField()
    Duration_Min_Time=forms.IntegerField()