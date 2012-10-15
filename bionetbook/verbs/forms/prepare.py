from verbs.baseforms import forms


class PrepareForm(forms.VerbForm):

    name = "prepare"
    slug = "prepare"


    edit_what_remark = forms.CharField()
    comment_why = forms.CharField()
    duration_min_time = forms.IntegerField()
    describe_where = forms.CharField()
    edit_caution_or_warning = forms.CharField()
    edit_remarks = forms.CharField()
    specify_tool = forms.CharField()
    specify_date = forms.DateField()