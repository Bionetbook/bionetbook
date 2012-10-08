from verbs.baseforms import forms


class SuspendForm(forms.VerbForm):

    name = "Suspend"
    slug = "Suspend"


    Duration_Min_Time=forms.IntegerField()