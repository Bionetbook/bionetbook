from verbs.baseforms import forms


class PourForm(forms.VerbForm):

    name = "pour"
    slug = "pour"


    Edit_what_remark=forms.CharField()
    Describe_where=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Add_conditional_statement=forms.CharField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Comment_why=forms.CharField()