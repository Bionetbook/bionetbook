from verbs.baseforms import forms


class CentrifugeForm(forms.VerbForm):

    name = "Centrifuge"
    slug = "centrifuge"

    edit_what_remark = forms.CharField()
    min_spin_speed = forms.IntegerField()
    max_spin_speed = forms.IntegerField()
    comment_why = forms.CharField()
    duration_min_time = forms.IntegerField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
