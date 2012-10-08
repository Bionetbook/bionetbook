from verbs.baseforms import forms


class RemoveForm(forms.VerbForm):

    name = "remove"
    slug = "remove"


    Edit_what_remark=forms.CharField()
    Specify_tool=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Specify_date=forms.DateField()