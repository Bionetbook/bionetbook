from verbs.baseforms import forms


class MixForm(forms.VerbForm):

    name = "mix"
    slug = "mix"


    Duration_Min_Time=forms.IntegerField()
    Comment_why=forms.CharField()
    Edit_remarks=forms.CharField()