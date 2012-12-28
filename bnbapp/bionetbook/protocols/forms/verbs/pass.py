from protocols import forms


class PassForm(forms.VerbForm):

    name = "Pass"
    slug = "pass"

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
    add_with_what = forms.CharField()
    specify_number_of_times = forms.IntegerField()
