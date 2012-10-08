from verbs.baseforms import forms


class SwitchoffForm(forms.VerbForm):

    name = "Switchoff"
    slug = "Switchoff"


    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Duration_Min_Time=forms.IntegerField()
    Edit_kit_name=forms.CharField()
    Edit_protocol_output=forms.CharField()
    Edit_remarks=forms.CharField()