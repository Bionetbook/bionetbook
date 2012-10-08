from verbs.baseforms import forms


class CombineForm(forms.VerbForm):

    name = "combine"
    slug = "combine"


    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Duration_Min_Time=forms.IntegerField()
    Describe_where=forms.CharField()
    Edit_remarks=forms.CharField()