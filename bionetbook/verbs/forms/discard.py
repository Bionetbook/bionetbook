from verbs.baseforms import forms


class DiscardForm(forms.VerbForm):

    name = "discard"
    slug = "discard"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Describe_where=forms.CharField()
    Edit_remarks=forms.CharField()
    Edit_why_step=forms.CharField()