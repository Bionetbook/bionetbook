from verbs.baseforms import forms


class WeighForm(forms.VerbForm):

    name = "weigh"
    slug = "weigh"


    Edit_what_remark=forms.CharField()
    Edit_vessel_type=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Describe_where=forms.CharField()
    Edit_remarks=forms.CharField()
    Specify_machine=forms.CharField()
    Edit_why_step=forms.CharField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()