from protocols.forms import forms


class LetSitStandForm(forms.VerbForm):

    name = "Let Sit/Stand"
    slug = "let-sit-stand"

    duration_in_seconds = forms.IntegerField()
