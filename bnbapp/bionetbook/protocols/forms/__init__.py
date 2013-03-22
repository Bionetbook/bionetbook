import floppyforms as forms
from organization.models import Organization
from core.utils import CONCENTRATION_UNITS, VOLUME_UNITS, TIME_UNITS, SPEED_UNITS, TEMPERATURE_UNITS, AMMOUNT_UNITS


class NodeForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    remark = forms.CharField(label='Comment', required=False, initial ='phase of protocol')


class OrganizationListForm(forms.Form):
    owner = forms.ChoiceField(required=True)#forms.CharField(max_length=100, required=False)


class ProtocolPublishForm(forms.Form):
    name = forms.BooleanField(label='Confirm')


class StepForm(NodeForm):
    pass


class ActionForm(NodeForm):

    name = forms.CharField(max_length=100, required=False, help_text = 'describe phase')
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    time_units = forms.CharField(initial='seconds', required=False)
    # duration_comment = forms.ChoiceField(choices = (("Passive","You dont have to be here"),("Active","You are here"),), required=False)
    tube = forms.CharField(initial ='Name for tube: Sample | Mix | Buffer', required=False)
    why = forms.CharField(required=False, initial = 'why are you doing this?')

class VerbForm(forms.Form):
    has_component = False
    has_machine = False
    has_thermocycler = False

forms.VerbForm = VerbForm


class ComponentForm(NodeForm):

    reagent_name = forms.CharField(max_length=100, required=False)
    conc_units = forms.ChoiceField(required=False, choices=CONCENTRATION_UNITS )
    vol_units = forms.ChoiceField(required=False, choices=VOLUME_UNITS )
    ammount_units = forms.ChoiceField(required=False, choices = AMMOUNT_UNITS)
    min_conc = forms.FloatField(required=False)
    max_conc = forms.FloatField(required=False)
    min_vol = forms.FloatField(required=False)
    max_vol = forms.FloatField(required=False)
    min_vol = forms.FloatField(required=False)
    max_vol = forms.FloatField(required=False)
    source = forms.CharField(required=False, initial = 'Invitrogen')
    # ph = forms.FloatField()


class MachineForm(NodeForm):

    name = forms.CharField(required=False)
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, initial = 's' )
    min_time = forms.FloatField(required=False)
    max_time = forms.FloatField(required=False)
    time_comment = forms.CharField(required=False)
    # min_speed = forms.FloatField()
    # max_speed = forms.FloatField()
    min_temp = forms.FloatField(required=False, initial = 22.0)
    max_temp = forms.FloatField(required=False, initial = 22.0)
    temp_units = forms.ChoiceField(required=False, choices=TEMPERATURE_UNITS, initial = 'c')
    temp_comment = forms.CharField(required=False)
    # speed_units = forms.ChoiceField(required=False, choices=SPEED_UNITS )
    # speed_comment = forms.CharField(required=False)
    
    


class ThermocyclerForm(NodeForm):

    phase_name = forms.CharField(required=False, initial = 'Initiaion denaturation')
    min_temp = forms.FloatField()
    max_temp = forms.FloatField()
    min_time = forms.FloatField()
    max_time = forms.FloatField()
    cycles = forms.IntegerField()
    cycle_back_to = forms.ChoiceField(required=False, choices = range(1,10))
