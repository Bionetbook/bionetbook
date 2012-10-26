from verbs.baseforms import forms


class TransferForm(forms.VerbForm):

    name = "transfer"
    slug = "transfer"

    describe_where = forms.CharField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    duration_min_time = forms.IntegerField()
    comment_why = forms.CharField()
    edit_kit_name = forms.CharField()
    edit_protocol_output = forms.CharField()
    edit_remarks = forms.CharField()
    edit_what_remark = forms.CharField()
    specify_machine = forms.CharField()
    min_spin_speed = forms.IntegerField()
    max_spin_speed = forms.IntegerField()
    edit_why_step = forms.CharField()
