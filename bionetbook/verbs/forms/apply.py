from verbs.baseforms import forms


class ApplyForm(forms.VerbForm):

    name = "apply"
    slug = "apply"


    Edit_what_remark=forms.CharField()
    Describe_where=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Edit_remarks=forms.CharField()
    Specify_tool=forms.CharField()
    Comment_why=forms.CharField()