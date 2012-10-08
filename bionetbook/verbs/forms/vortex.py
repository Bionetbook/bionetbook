from verbs.baseforms import forms


class VortexForm(forms.VerbForm):

    name = "vortex"
    slug = "vortex"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Comment_why=forms.CharField()
    Describe_where=forms.CharField()