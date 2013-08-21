import floppyforms as forms
from organization.models import Organization
from core.utils import CONCENTRATION_UNITS, VOLUME_UNITS, TIME_UNITS, SPEED_UNITS, TEMPERATURE_UNITS, MASS_UNITS, AMMOUNT_UNITS


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
    # tube_label = forms.CharField(help_text ='copy label of tube', required=False)
    # describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    # min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    # max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    # time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds' )
    # time_comment = forms.CharField(required=False)
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

    #reagent_name = forms.CharField(max_length=100, required=False)                 # THIS IS COVERED WITH THE name FIELD
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
    # tube_label = forms.CharField(help_text ='label of component, not sample', required=False)  
    # technique_comment = forms.CharField(required=False, help_text='describe technique tips, help, comments, dont describe chemistry or biology')
    # why = forms.CharField(required=False, help_text='scientific reason you\'re doing this?')
    # ph = forms.FloatField()


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
    # technique_comment = forms.CharField(required=False, help_text='describe technique tips, help, comments, dont describe chemistry or biology')
    # why = forms.CharField(required=False, help_text='scientific reason you\'re doing this?')

class ThermocyclerForm(NodeForm):

    # phase_name = forms.CharField(required=False, help_text='example: Initiaion denaturation')
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



'''
    aliquot_volume = forms.IntegerField()
    aliquot_concentration = forms.IntegerField()
    aliquote_what = forms.CharField(help_text = 'name of reagent or mix')
    apply_action_to = forms.CharField(help_text = 'what are you doing the action on?')    
    concentration_units = forms.ChoiceField(choices = CONCENTRATION_UNITS)
    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    number_of_times = forms.IntegerField(required = False)
    number_of_aliquots = forms.IntegerField(help_text = 'number of tubes you are aliquoting into')
    min_time = forms.IntegerField()
    max_time = forms.IntegerField()
    time_units = forms.ChoiceField(choices = TIME_UNITS, intial = 's')
    remarks = forms.CharField(required = False)
    specify_tool = forms.CharField(required = False, help_text = 'not machine, scissors, pippete, blade etc')
    vessel_type = forms.ChoiceField(required = False, choices = VESSELS)
    volume_units = forms.ChoiceField(choices = VOLUME_UNITS)
    using_what = forms.CharField(required = False, help_text = 'rotator, shaker, manual etc')

    to delete:
    comment_why = forms.CharField(required = False)
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')


'''