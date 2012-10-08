from verbs.baseforms import forms


class GrindForm(forms.VerbForm):

    name = "grind"
    slug = "grind"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()