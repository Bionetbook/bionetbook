from verbs.baseforms import forms


class ActionForm(forms.VerbForm):

    name = "action" # cannot silence the name without an error, the name here is redundant
    slug = "action"


    Duration_Min_Time=forms.IntegerField()
    Comment_why=forms.CharField()
    Edit_What_to=forms.CharField()
    Edit_vessel_type=forms.CharField()
    Specify_number_of_times=forms.IntegerField()