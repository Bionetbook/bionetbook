from protocols.forms import forms


class RemoveForm(forms.VerbForm):

    name = "Remove"
    slug = "remove"

    edit_what_remark = forms.CharField()
    specify_tool = forms.CharField()
    duration_min_time = forms.IntegerField()
    specify_date = forms.DateField()
