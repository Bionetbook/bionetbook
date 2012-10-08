from verbs.baseforms import forms


class DecantForm(forms.VerbForm):

    name = "decant"
    slug = "decant"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()