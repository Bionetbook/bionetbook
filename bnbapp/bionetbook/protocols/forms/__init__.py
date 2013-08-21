import floppyforms as forms
from organization.models import Organization
from core.utils import CONCENTRATION_UNITS, VOLUME_UNITS, TIME_UNITS, SPEED_UNITS, TEMPERATURE_UNITS, MASS_UNITS, AMMOUNT_UNITS
from django.core.exceptions import ValidationError

###########
# REGEX PATTERNS
###########

validTimeFormat = re.compile('(\d+\:\d+\:\d+)|(\d+\:\d+)|(\d+)')

###########
# VALIDATORS
###########

def validateTimeFormat(value):
    error = False
    times = value.split("-")

    if len(times) > 2:
        error = True

    for time in times:
        if not validTimeFormat.match(time):
            error = True

    if error:
        raise ValidationError(u"'%s' has to be in a common time format such as 'Seconds', 'MM:SS', 'HH:MM:SS' or range such as 'maxtime-mintime'" % value)


###########
# FROMS
###########

class NodeForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    technique_comment = forms.CharField(required=False, help_text='describe technique tips, or help')
    why = forms.CharField(required=False, help_text='scientific reason you\'re doing this?')


class OrganizationListForm(forms.Form):
    owner = forms.ChoiceField(required=True)#forms.CharField(max_length=100, required=False)


class ProtocolPublishForm(forms.Form):
    name = forms.BooleanField(label='Confirm')


class StepForm(NodeForm):
    name = forms.CharField(max_length=100, required=False, label='Step Name')
    verbatim_text = forms.CharField(required=False, label='Verbatim Text', help_text='As written text from the protocol (if you are transposing from another source)')


class ActionForm(NodeForm):
    name = forms.CharField(max_length=100, required=False, help_text = 'This will autofill')
    tracking_object = forms.CharField(required=False, help_text='Sample mix | Buffer | Other mix')
    min_temp = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))#, initial = 22.0)
    max_temp = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))#, initial = 22.0)
    temp_units = forms.ChoiceField(required=False, choices=TEMPERATURE_UNITS, help_text='in celcius')
    temp_comment = forms.CharField(required=False)
    physical_commitment = forms.ChoiceField(choices = (("N/A","unknown"),("Passive","You dont have to be here"),("Active","You are here"),('Setup', 'only required to start'), ('missing','no description present'),), required=False)


class VerbForm(forms.Form):
    has_component = False
    has_machine = False
    has_thermocycler = False
    has_manual = False
    layers = []


forms.VerbForm = VerbForm


class ComponentForm(NodeForm):
    min_conc = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    max_conc = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    conc_units = forms.ChoiceField(required=False, choices=CONCENTRATION_UNITS )
    conc_comment = forms.CharField(required=False)
    min_vol = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    max_vol = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    vol_units = forms.ChoiceField(required=False, choices=VOLUME_UNITS )
    vol_comment = forms.CharField(required=False)
    min_mass = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    max_mass = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    mass_units = forms.ChoiceField(required=False, choices = MASS_UNITS, initial = None)
    min_ammount = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    max_ammount = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    ammount_units = forms.ChoiceField(required=False, choices = AMMOUNT_UNITS, initial = None)
    source = forms.CharField(required=False, help_text='example: Invitrogen | protocol: RNA purification')
    ph = forms.FloatField(required=False, help_text='only if specified', widget=forms.NumberInput(attrs={'step':'any'}))
    tracking_object = forms.CharField(required=False, help_text='Name for tube: Sample | Mix | Buffer')


class MachineForm(NodeForm):
    name = forms.CharField(required=False)
    model = forms.CharField(required=False, help_text='only if it really matters')
    min_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds' )
    time_comment = forms.CharField(required=False)
    min_temp = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))#, initial = 22.0)
    max_temp = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))#, initial = 22.0)
    temp_units = forms.ChoiceField(required=False, choices=TEMPERATURE_UNITS, help_text='in celcius')
    temp_comment = forms.CharField(required=False)
    min_speed = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    max_speed = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    speed_units = forms.ChoiceField(required=False, choices=SPEED_UNITS )
    speed_comment = forms.CharField(required=False)


class ThermocyclerForm(NodeForm):
    min_temp = forms.FloatField(widget=forms.NumberInput(attrs={'step':'any'}))
    max_temp = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    temp_units = forms.ChoiceField(required=False, choices=TEMPERATURE_UNITS, help_text='in celcius')
    min_time = forms.FloatField(widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, initial='sec' )
    time_comment = forms.CharField(required=False)
    cycles = forms.IntegerField(required=False)
    phase_list= [('','no cycle back')]
    phase_list.extend([(x,x) for x in range(1,10)])
    cycle_back_to = forms.ChoiceField(required=False, choices=phase_list, initial='')


