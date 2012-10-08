from verbs.baseforms import forms


class TransferForm(forms.VerbForm):

    name = "transfer"
    slug = "transfer"


    Describe_where=forms.CharField()
    Min_Temp=forms.IntegerField()
    Max_Temp=forms.IntegerField()
    Duration_Min_Time=forms.IntegerField()
    Comment_why=forms.CharField()
    Edit_kit_name=forms.CharField()
    Edit_protocol_output=forms.CharField()
    Edit_remarks=forms.CharField()
    Edit_what_remark=forms.CharField()
    Specify_machine=forms.CharField()
    Min_Spin_Speed=forms.IntegerField()
    Max_Spin_Speed=forms.IntegerField()
    Edit_why_step=forms.CharField()