from verbs.baseforms import forms


class CoolForm(forms.VerbForm):

    name = "cool"
    slug = "cool"


    Edit_remarks=forms.CharField()
    Edit_what_remark=forms.CharField()
    Specify_machine=forms.CharField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Specify_date=forms.DateField()
    Comment_why=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Add_conditional_statement=forms.CharField()