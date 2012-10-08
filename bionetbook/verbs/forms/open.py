from verbs.baseforms import forms


class OpenForm(forms.VerbForm):

    name = "open"
    slug = "open"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Describe_where=forms.CharField()