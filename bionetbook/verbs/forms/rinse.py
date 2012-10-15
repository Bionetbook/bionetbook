from verbs.baseforms import forms


class RinseForm(forms.VerbForm):

    name = "rinse"
    slug = "rinse"


    edit_what_remark = forms.CharField()
    add_with_what = forms.CharField()
    duration_min_time = forms.IntegerField()
    edit_into = forms.CharField()