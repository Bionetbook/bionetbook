from verbs.baseforms import forms


class GrowForm(forms.VerbForm):

    name = "grow"
    slug = "grow"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Edit_What_to=forms.CharField()
    Edit_vessel_type=forms.CharField()
    Edit_remarks=forms.CharField()
    Describe_where=forms.CharField()
    Specify_date=forms.DateField()
    Comment_why=forms.CharField()