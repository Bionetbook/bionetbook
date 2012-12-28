from protocols import forms


class PrecipitateForm(forms.VerbForm):

    name = "Precipitate"
    slug = "precipitate"

    edit_what_remark = forms.CharField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    duration_min_time = forms.IntegerField()
