from verbs.baseforms import forms


class CoverForm(forms.VerbForm):

    name = "cover"
    slug = "cover"


    Add_conditional_statement=forms.CharField()
    Edit_what_remark=forms.CharField()
    Comment_why=forms.CharField()
    Duration_Min_Time=forms.IntegerField()