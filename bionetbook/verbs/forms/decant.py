from verbs.baseforms import forms


class DecantForm(forms.VerbForm):

    name = "decant"
    slug = "decant"


    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()