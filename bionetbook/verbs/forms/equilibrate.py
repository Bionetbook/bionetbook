from verbs.baseforms import forms


class EquilibrateForm(forms.VerbForm):

    name = "equilibrate"
    slug = "equilibrate"


    Edit_what_remark=forms.CharField()
    Add_with_what=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Edit_What_to=forms.CharField()