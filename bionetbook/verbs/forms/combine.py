from verbs.baseforms import forms


class CombineForm(forms.VerbForm):

    name = "combine"
    slug = "combine"


    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    duration_min_time = forms.IntegerField()
    describe_where = forms.CharField()
    edit_remarks = forms.CharField()