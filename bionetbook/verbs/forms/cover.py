from verbs.baseforms import forms


class CoverForm(forms.VerbForm):

    name = "cover"
    slug = "cover"


    add_conditional_statement = forms.CharField()
    edit_what_remark = forms.CharField()
    comment_why = forms.CharField()
    duration_min_time = forms.IntegerField()