from verbs.baseforms import forms


class PouroffForm(forms.VerbForm):

    name = "Pouroff"
    slug = "Pouroff"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()