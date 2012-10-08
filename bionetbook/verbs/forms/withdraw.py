from verbs.baseforms import forms


class WithdrawForm(forms.VerbForm):

    name = "withdraw"
    slug = "withdraw"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Describe_where=forms.CharField()