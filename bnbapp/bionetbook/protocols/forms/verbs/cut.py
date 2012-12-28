from protocols import forms


class CutForm(forms.VerbForm):

    name = "Cut"
    slug = "cut"


    edit_what_remark = forms.CharField()
    duration_min_time = forms.IntegerField()
    comment_why = forms.CharField()