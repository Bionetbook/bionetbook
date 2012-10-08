from verbs.baseforms import forms


class TreatForm(forms.VerbForm):

    name = "treat"
    slug = "treat"


    Edit_what_remark=forms.CharField()
    Edit_machine_settings=forms.CharField()
    Duration_Min_Time=forms.IntegerField()