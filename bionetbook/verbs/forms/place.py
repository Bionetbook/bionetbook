from verbs.baseforms import forms


class PlaceForm(forms.VerbForm):

    name = "place"
    slug = "place"


    Edit_what_remark=forms.CharField()
    Describe_where=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Add_conditional_statement=forms.CharField()