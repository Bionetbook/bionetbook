from protocols.forms import forms


class RepeatForm(forms.VerbForm):

    name = "Repeat"
    slug = "repeat"

    edit_what_remark = forms.CharField()
    add_with_what = forms.CharField()
    duration_min_time = forms.IntegerField()
    describe_where = forms.CharField()
    edit_remarks = forms.CharField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    specify_machine = forms.CharField()
    edit_why_step = forms.CharField()
