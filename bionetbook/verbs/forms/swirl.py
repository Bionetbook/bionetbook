from verbs.baseforms import forms


class SwirlForm(forms.VerbForm):

    name = "swirl"
    slug = "swirl"


    Comment_why=forms.CharField()
    Duration_Min_Time=forms.IntegerField()