from verbs.baseforms import forms


class RepeatForm(forms.VerbForm):

    name = "repeat"
    slug = "repeat"


    Edit_what_remark=forms.CharField()
    Add_with_what=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Describe_where=forms.CharField()
    Edit_remarks=forms.CharField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Specify_machine=forms.CharField()
    Edit_why_step=forms.CharField()