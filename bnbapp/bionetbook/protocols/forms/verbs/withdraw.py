from verbs.baseforms import forms


class WithdrawForm(forms.VerbForm):

    name = "Withdraw"
    slug = "withdraw"

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
    describe_where = forms.CharField()
