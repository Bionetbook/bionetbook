from verbs.baseforms import forms


class ChillForm(forms.VerbForm):

    name = "chill"
    slug = "chill"


    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Duration_Min_Time=forms.IntegerField()
    Edit_remarks=forms.CharField()
    Describe_where=forms.CharField()