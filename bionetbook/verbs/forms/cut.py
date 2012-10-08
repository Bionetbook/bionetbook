from verbs.baseforms import forms


class CutForm(forms.VerbForm):

    name = "cut"
    slug = "cut"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Comment_why=forms.CharField()