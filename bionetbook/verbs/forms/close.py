from verbs.baseforms import forms


class CloseForm(forms.VerbForm):

    name = "close"
    slug = "close"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()