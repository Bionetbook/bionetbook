from protocols import forms


class PourForm(forms.VerbForm):

    name = "Pour"
    slug = "pour"

    edit_what_remark = forms.CharField()
    describe_where = forms.CharField()
    duration_min_time = forms.IntegerField()
    add_conditional_statement = forms.CharField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    comment_why = forms.CharField()
