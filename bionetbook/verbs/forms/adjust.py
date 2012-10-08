from verbs.baseforms import forms


class AdjustForm(forms.VerbForm):

    name = "Adjust"
    slug = "Adjust"


    Edit_what_remark=forms.CharField()
    Add_conditional_statement=forms.CharField()
    Specify_machine=forms.CharField()
    Duration_Min_Time=forms.IntegerField()