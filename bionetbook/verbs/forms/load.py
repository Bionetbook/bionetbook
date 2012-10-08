from verbs.baseforms import forms


class LoadForm(forms.VerbForm):

    name = "load"
    slug = "load"


    Describe_where=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Edit_what_remark=forms.CharField()