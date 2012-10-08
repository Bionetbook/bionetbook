from verbs.baseforms import forms


class DryForm(forms.VerbForm):

    name = "dissolve"
    slug = "dissolve"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()