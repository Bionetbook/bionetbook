from protocols.forms import forms
SPEED_UNITS = (("rpm","Revolutions Per Minutes"),("rcf","Relative Centrifugal Force"),)

class SpinForm(forms.VerbForm):

    name = "Spin"
    slug = "spin"
    has_machine = True

    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    min_speed = forms.IntegerField()
    max_speed = forms.IntegerField(required = False)
    speed_units = forms.ChoiceField(required=False, choices = SPEED_UNITS, initial = 'rpm' )
    speed_comment = forms.CharField(required=False)
    comment_why = forms.CharField(required = False)
