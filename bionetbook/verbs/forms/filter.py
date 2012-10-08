from verbs.baseforms import forms


class FilterForm(forms.VerbForm):

    name = "filter"
    slug = "filter"


    Comment_why=forms.CharField()
    Duration_Min_Time=forms.IntegerField()