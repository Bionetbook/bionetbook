from verbs.baseforms import forms


class PassForm(forms.VerbForm):

    name = "pass"
    slug = "pass"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Add_with_what=forms.CharField()
    Specify_number_of_times=forms.IntegerField()