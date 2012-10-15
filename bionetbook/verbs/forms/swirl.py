from verbs.baseforms import forms


class SwirlForm(forms.VerbForm):

    name = "swirl"
    slug = "swirl"


    comment_why = forms.CharField()
    duration_min_time = forms.IntegerField()