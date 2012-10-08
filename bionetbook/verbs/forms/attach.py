from verbs.baseforms import forms


class AttachForm(forms.VerbForm):

    name = "attach"
    slug = "attach"


    Edit_what_remark=forms.CharField()
    Describe_where=forms.CharField()
    Duration_Min_Time=forms.IntegerField()