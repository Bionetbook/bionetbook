
from protocols.forms import forms


class VortexForm(forms.VerbForm):

    name = "Vortex"
    slug = "vortex"
    has_machine = True

    # edit_what_remark = forms.CharField()
    # duration_min_time = forms.IntegerField()
    # comment_why = forms.CharField()
    describe_where = forms.CharField(required = False)
