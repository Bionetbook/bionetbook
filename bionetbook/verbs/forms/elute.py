from verbs.baseforms import forms


class EluteForm(forms.VerbForm):

    name = "elute"
    slug = "elute"


    Edit_what_remark=forms.CharField()
    Edit_into=forms.CharField()
    Add_with_what=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Edit_remarks=forms.CharField()