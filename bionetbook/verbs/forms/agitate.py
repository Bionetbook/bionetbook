from verbs.baseforms import forms


class AgitateForm(forms.VerbForm):

    name = "agitate"
    slug = "agitate"


    Duration_Min_Time=forms.IntegerField()
    Add_conditional_statement=forms.CharField()
    Edit_what_remark=forms.CharField()
    Comment_why=forms.CharField()
    Describe_where=forms.CharField()
    Edit_remarks=forms.CharField()
    Add_with_what=forms.CharField()