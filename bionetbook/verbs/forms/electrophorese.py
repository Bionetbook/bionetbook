from verbs.baseforms import forms


class ElectrophoreseForm(forms.VerbForm):

    name = "electrophorese"
    slug = "electrophorese"


    Edit_remarks=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Specify_machine=forms.CharField()
    Min_Voltage=forms.IntegerField()
    Max_Voltage=forms.IntegerField()