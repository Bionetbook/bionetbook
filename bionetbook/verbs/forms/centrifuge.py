from verbs.baseforms import forms


class CentrifugeForm(forms.VerbForm):

    name = "Centrifuge"
    slug = "Centrifuge"


    Edit_what_remark=forms.CharField()
    Min_Spin_Speed=forms.IntegerField()
    Max_Spin_Speed=forms.IntegerField()
    Comment_why=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()