from protocols import forms


class SealForm(forms.VerbForm):

    name = "Seal"
    slug = "seal"

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
    describe_where = forms.CharField()
    edit_why_step = forms.CharField()
    edit_remarks = forms.CharField()
    specify_machine = forms.CharField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
