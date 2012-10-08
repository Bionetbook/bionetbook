from verbs.baseforms import forms


class SealForm(forms.VerbForm):

    name = "seal"
    slug = "seal"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Describe_where=forms.CharField()
    Edit_why_step=forms.CharField()
    Edit_remarks=forms.CharField()
    Specify_machine=forms.CharField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()