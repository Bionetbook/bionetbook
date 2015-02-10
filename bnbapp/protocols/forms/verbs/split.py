from protocols.forms import forms


class SplitForm(forms.VerbForm):

    name = "Split"
    slug = "split"

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    edit_remarks = forms.CharField()
    add_with_what = forms.CharField()
