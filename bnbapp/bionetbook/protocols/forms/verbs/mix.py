from protocols.forms import forms


class MixForm(forms.VerbForm):

    name = "Mix"
    slug = "mix"
    has_manual = True
    layers = ['technique_comment','duration','duration_units']
    # duration_min_time = forms.IntegerField()
    # comment_why = forms.CharField()
    # edit_remarks = forms.CharField()
