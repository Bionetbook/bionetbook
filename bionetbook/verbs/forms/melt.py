from verbs.baseforms import forms


class MeltForm(forms.VerbForm):

    name = "melt"
    slug = "melt"


    Edit_what_remark=forms.CharField()
    Specify_machine=forms.CharField()
    Duration_Min_Time=forms.IntegerField()