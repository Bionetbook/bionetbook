
from verbs.baseforms import forms


class AddForm(forms.VerbForm):

    name = "add" # cannot silence the name without an error, the name here is redundant
    slug = "add"

    Duration_Min_Time=forms.IntegerField()
    Describe_where=forms.CharField()
    Edit_remarks=forms.CharField()