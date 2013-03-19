from protocols.forms import forms


class CentrifugeForm(forms.VerbForm):

    name = "Centrifuge"
    slug = "centrifuge"
    has_machine = True

    handled_object = forms.CharField(required = False, initial = 'Name for tube: Sample | Mix | Buffer')
    min_speed = forms.IntegerField()
    max_speed = forms.IntegerField(required = False)
    # comment_why = forms.CharField()
    min_time = forms.IntegerField()
    max_time = forms.IntegerField(required = False)
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField(required = False)
    time_units = forms.CharField(required=False, initial = 'Seconds' )
    temp_units = forms.CharField(required=False, initial = "Celcius" )
    speed_units = forms.CharField(required=False, initial = 'RPM' )
    speed_comment = forms.CharField(required=False)
    temp_comment = forms.CharField(required=False)
    time_comment = forms.CharField(required=False)
