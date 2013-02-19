import floppyforms as forms

#from protocols.forms.baseforms import ProtocolForm

from protocols.models import Protocol
from organization.models import Organization

CONCENTRATION_UNITS = (("l","Liter"),("ml","Microliter"),)
VOLUME_UNITS = (("l","Liter"),("ml","Microliter"),)
TIME_UNITS = (("m","Minutes"),("s","Seconds"),)
SPEED_UNITS = (("rpm","Revolutions Per Minutes"),("rps","Revolutions Per Seconds"),)
TEMPERATURE_UNITS = (("c","Celsius"),("k","Kelvin"),("f","Ferinheit"),)


class NodeForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    remark = forms.CharField(label='Comment', required=False)


class ProtocolForm(forms.ModelForm):

    class Meta:
        model = Protocol
        exclude = ('parent', 'slug', 'duration_in_seconds', 'status', 'version','raw')

    def __init__(self, *args, **kwargs):
        super(ProtocolForm, self).__init__(*args, **kwargs)
        choices = [(pt.id, unicode(pt.name)) for pt in Organization.objects.all()]
        self.fields['owner'].choices = choices


class ProtocolPublishForm(forms.Form):
    name = forms.BooleanField(label='Confirm')


class StepForm(NodeForm):
    pass


class ActionForm(NodeForm):

    time_units = forms.CharField(required=False)
    duration = forms.IntegerField()
    duration_comment = forms.CharField(required=False)


class VerbForm(forms.Form):
    has_components = False
    has_machines = False
    has_thermocycler = False

forms.VerbForm = VerbForm


class ComponentForm(NodeForm):

    reagent_name = forms.CharField(max_length=100, required=False)
    conc_units = forms.ChoiceField(required=False, choices=CONCENTRATION_UNITS )
    vol_units = forms.ChoiceField(required=False, choices=VOLUME_UNITS )
    min_conc = forms.FloatField()
    max_conc = forms.FloatField()
    min_vol = forms.FloatField()
    max_vol = forms.FloatField()
    ph = forms.FloatField()


class MachineForm(NodeForm):

    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS )
    min_time = forms.FloatField()
    max_time = forms.FloatField()
    min_speed = forms.FloatField()
    max_speed = forms.FloatField()
    min_temp = forms.FloatField()
    max_temp = forms.FloatField()
    temp_units = forms.ChoiceField(required=False, choices=TEMPERATURE_UNITS )
    speed_units = forms.ChoiceField(required=False, choices=SPEED_UNITS )
    speed_comment = forms.CharField(required=False)
    temp_comment = forms.CharField(required=False)
    time_comment = forms.CharField(required=False)


class ThermocyclerForm(NodeForm):
    min_time = forms.FloatField()
    max_time = forms.FloatField()
