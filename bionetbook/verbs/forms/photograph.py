from verbs.baseforms import forms


class PhotographForm(forms.VerbForm):

    name = "photograph"
    slug = "photograph"


    Edit_what_remark=forms.CharField()
    Edit_remarks=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Specify_date=forms.DateField()