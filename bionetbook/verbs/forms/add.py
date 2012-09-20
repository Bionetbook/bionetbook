from verbs.baseforms import forms


class AddForm(forms.VerbForm):

    name = "add"
    slug = "add"

    duration_in_seconds = forms.IntegerField()
    amount = forms.IntegerField()
    substance = forms.CharField()
    add_a_text_remark = forms.CharField()
