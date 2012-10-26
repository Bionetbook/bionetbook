from verbs.baseforms import forms


class AdjustForm(forms.VerbForm):

    name = "Adjust"
    slug = "adjust"

    edit_what_remark = forms.CharField()
    add_conditional_statement = forms.CharField()
    specify_machine = forms.CharField()
    duration_min_time = forms.IntegerField()
