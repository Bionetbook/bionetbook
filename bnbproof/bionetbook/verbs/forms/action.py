from verbs.baseforms import forms


class ActionForm(forms.VerbForm):

    name = "Action" # cannot silence the name without an error, the name here is redundant
    slug = "action"

    duration_min_time = forms.IntegerField()
    comment_why = forms.CharField()
    edit_what_to = forms.CharField()
    edit_vessel_type = forms.CharField()
    specify_number_of_times = forms.IntegerField()
