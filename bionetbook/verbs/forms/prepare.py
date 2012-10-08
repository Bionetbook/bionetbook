from verbs.baseforms import forms


class PrepareForm(forms.VerbForm):

    name = "prepare"
    slug = "prepare"


    Edit_what_remark=forms.CharField()
    Comment_why=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Describe_where=forms.CharField()
    Edit_caution_or_warning=forms.CharField()
    Edit_remarks=forms.CharField()
    Specify_tool=forms.CharField()
    Specify_date=forms.DateField()