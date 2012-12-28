from protocols import forms


class ApplyForm(forms.VerbForm):

    name = "Apply"
    slug = "apply"

    edit_what_remark = forms.CharField()
    describe_where = forms.CharField()
    duration_min_time = forms.IntegerField()
    edit_remarks = forms.CharField()
    specify_tool = forms.CharField()
    comment_why = forms.CharField()
