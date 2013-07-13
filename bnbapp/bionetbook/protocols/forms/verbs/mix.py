from protocols.forms import forms


class MixForm(forms.VerbForm):

    name = "Mix"
    slug = "mix"
    has_manual = True
    layers = ['settify']
    # duration_min_time = forms.IntegerField()
    # comment_why = forms.CharField()
    # edit_remarks = forms.CharField()
