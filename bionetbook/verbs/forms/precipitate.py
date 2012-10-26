from verbs.baseforms import forms


class PrecipitateForm(forms.VerbForm):

    name = "precipitate"
    slug = "precipitate"

    edit_what_remark = forms.CharField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    duration_min_time = forms.IntegerField()
