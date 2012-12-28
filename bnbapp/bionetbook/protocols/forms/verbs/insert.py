from protocols.forms import forms


class InsertForm(forms.VerbForm):

    name = "insert"
    slug = "insert"


    edit_what_remark = forms.CharField()
    describe_where = forms.CharField()
    specify_machine = forms.CharField()
    duration_min_time = forms.IntegerField()
    edit_remarks = forms.CharField()
    edit_why_step = forms.CharField()
    edit_from = forms.CharField()
    specify_tool = forms.CharField()