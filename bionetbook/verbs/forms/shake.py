from verbs.baseforms import forms


class ShakeForm(forms.VerbForm):

    name = "shake"
    slug = "shake"


    Edit_remarks=forms.CharField()
    Add_conditional_statement=forms.CharField()
    Edit_what_remark=forms.CharField()
    Comment_why=forms.CharField()
    Duration_Min_Time=forms.IntegerField()