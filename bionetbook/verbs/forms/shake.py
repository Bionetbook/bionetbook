from verbs.baseforms import forms


class ShakeForm(forms.VerbForm):

    name = "shake"
    slug = "shake"


    edit_remarks = forms.CharField()
    add_conditional_statement = forms.CharField()
    edit_what_remark = forms.CharField()
    comment_why = forms.CharField()
    duration_min_time = forms.IntegerField()