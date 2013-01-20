from protocols.forms import forms


class AgitateForm(forms.VerbForm):

    name = "Agitate"
    slug = "agitate"
    has_machines = True


    duration_min_time = forms.IntegerField()
    add_conditional_statement = forms.CharField()
    edit_what_remark = forms.CharField()
    comment_why = forms.CharField()
    describe_where = forms.CharField()
    edit_remarks = forms.CharField()
    add_with_what = forms.CharField()
