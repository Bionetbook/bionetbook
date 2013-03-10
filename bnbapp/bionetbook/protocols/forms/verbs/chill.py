from protocols.forms import forms


class ChillForm(forms.VerbForm):

    name = "Chill"
    slug = "chill"
    has_machine = True

    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    duration_min_time = forms.IntegerField()
    edit_remarks = forms.CharField()
    describe_where = forms.CharField()
