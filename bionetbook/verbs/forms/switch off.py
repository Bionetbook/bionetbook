from verbs.baseforms import forms


class SwitchoffForm(forms.VerbForm):

    name = "Switchoff"
    slug = "Switchoff"


    Edit_remarks=forms.CharField()
    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Edit_why_step=forms.CharField()
    Describe_where=forms.CharField()
    Specify_machine=forms.CharField()