from protocols.forms import forms


class DecantForm(forms.VerbForm):

    name = "Decant"
    slug = "decant"
    has_machine = True

    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()