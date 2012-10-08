from verbs.baseforms import forms


class ResuspendForm(forms.VerbForm):

    name = "resuspend"
    slug = "resuspend"


    Edit_what_remark=forms.CharField()
    Add_with_what=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Edit_protocol_output=forms.CharField()
    Edit_remarks=forms.CharField()