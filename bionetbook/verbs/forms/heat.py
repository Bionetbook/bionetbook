from verbs.baseforms import forms


class HeatForm(forms.VerbForm):

    name = "heat"
    slug = "heat"


    Edit_what_remark=forms.CharField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Duration_Min_Time=forms.IntegerField()
    Edit_remarks=forms.CharField()