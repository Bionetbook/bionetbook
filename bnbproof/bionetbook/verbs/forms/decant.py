from verbs.baseforms import forms


class DecantForm(forms.VerbForm):

    name = "Decant"
    slug = "decant"


    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()