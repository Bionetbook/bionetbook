from verbs.baseforms import forms


class IncubateForm(forms.VerbForm):

    name = "incubate"
    slug = "incubate"


    Edit_what_remark=forms.CharField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Duration_Min_Time=forms.IntegerField()
    Comment_why=forms.CharField()
    Edit_remarks=forms.CharField()
    Edit_input =forms.CharField()
    Edit_protocol_output=forms.CharField()
    Edit_vessel_type=forms.CharField()
    Edit_kit_name=forms.CharField()