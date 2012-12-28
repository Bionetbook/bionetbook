from verbs.baseforms import forms


class CoolForm(forms.VerbForm):

    name = "Cool"
    slug = "cool"


    edit_remarks = forms.CharField()
    edit_what_remark = forms.CharField()
    specify_machine = forms.CharField()
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    specify_date = forms.DateField()
    comment_why = forms.CharField()
    duration_min_time = forms.IntegerField()
    add_conditional_statement = forms.CharField()