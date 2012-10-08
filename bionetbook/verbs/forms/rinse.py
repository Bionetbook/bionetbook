from verbs.baseforms import forms


class RinseForm(forms.VerbForm):

    name = "rinse"
    slug = "rinse"


    Edit_what_remark=forms.CharField()
    Add_with_what=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Edit_into=forms.CharField()