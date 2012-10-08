from verbs.baseforms import forms


class PrecipitateForm(forms.VerbForm):

    name = "precipitate"
    slug = "precipitate"


    Edit_what_remark=forms.CharField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Duration_Min_Time=forms.IntegerField()