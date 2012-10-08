from verbs.baseforms import forms


class DryForm(forms.VerbForm):

    name = "dry"
    slug = "dry"


    Duration_Min_Time=forms.IntegerField()
    Edit_what_remark=forms.CharField()
    Add_with_what=forms.CharField()