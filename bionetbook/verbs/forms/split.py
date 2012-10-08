from verbs.baseforms import forms


class SplitForm(forms.VerbForm):

    name = "split"
    slug = "split"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Edit_remarks=forms.CharField()
    Add_with_what=forms.CharField()