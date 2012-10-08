from verbs.baseforms import forms


class StoreForm(forms.VerbForm):

    name = "store"
    slug = "store"


    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Duration_Min_Time=forms.IntegerField()
    Edit_what_remark=forms.CharField()
    Edit_remarks=forms.CharField()
    Edit_vessel_type=forms.CharField()