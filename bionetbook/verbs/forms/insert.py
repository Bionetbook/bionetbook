from verbs.baseforms import forms


class InsertForm(forms.VerbForm):

    name = "insert"
    slug = "insert"


    Edit_what_remark=forms.CharField()
    Describe_where=forms.CharField()
    Specify_machine=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Edit_remarks=forms.CharField()
    Edit_why_step=forms.CharField()
    Edit_from=forms.CharField()
    Specify_tool=forms.CharField()