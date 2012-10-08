from verbs.baseforms import forms


class WashForm(forms.VerbForm):

    name = "wash"
    slug = "wash"


    Edit_what_remark=forms.CharField()
    Add_with_what=forms.CharField()
    Duration_Min_Time=forms.IntegerField()