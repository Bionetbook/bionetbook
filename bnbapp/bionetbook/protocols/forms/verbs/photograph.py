from protocols.forms import forms


class PhotographForm(forms.VerbForm):

    name = "photograph"
    slug = "photograph"
    has_machines = True

    edit_what_remark = forms.CharField()
    edit_remarks = forms.CharField()
    duration_min_time = forms.IntegerField()
    specify_date = forms.DateField()