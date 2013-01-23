import floppyforms as forms
from protocols.models import Protocol
from organization.models import Organization

class ProtocolForm(forms.ModelForm):

    class Meta:
        model = Protocol
        exclude = ('parent', 'slug', 'duration_in_seconds', 'status', 'version','raw')

    def __init__(self, *args, **kwargs):
        #user = kwargs.pop('user', None)
        super(ProtocolForm, self).__init__(*args, **kwargs)
        #choices=[]
        print kwargs

        #print user
        #choices = [(pt.id, unicode(pt.name)) for pt in PromotionType.objects.all()]
        #choices.extend(EXTRA_CHOICES)
        choices = [(pt.id, unicode(pt.name)) for pt in Organization.objects.all()]
        self.fields['owner'].choices = choices
        #self.fields['owner'].queryset = user.organization_set.all()
