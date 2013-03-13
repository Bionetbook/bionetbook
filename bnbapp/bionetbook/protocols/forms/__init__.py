import floppyforms as forms
from organization.models import Organization
from core.utils import CONCENTRATION_UNITS, VOLUME_UNITS, TIME_UNITS, SPEED_UNITS, TEMPERATURE_UNITS

class NodeForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    remark = forms.CharField(label='Comment', required=False, help_text ='phase of protocol')


class OrganizationListForm(forms.Form):
    owner = forms.ChoiceField(required=True)#forms.CharField(max_length=100, required=False)


class ProtocolPublishForm(forms.Form):
    name = forms.BooleanField(label='Confirm')


class StepForm(NodeForm):
    pass


class ActionForm(NodeForm):

    name = forms.CharField(max_length=100, required=False, help_text = 'Do not fill this in')
    duration = forms.IntegerField()
    time_units = forms.CharField(initial='seconds', required=False)
    duration_comment = forms.CharField(required=False)
    tube = forms.CharField(initial ='Name for tube: Sample | Mix | Buffer', required = False)


class VerbForm(forms.Form):
    has_component = False
    has_machine = False
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
