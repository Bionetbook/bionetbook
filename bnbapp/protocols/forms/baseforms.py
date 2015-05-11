import floppyforms as forms
from protocols.models import Protocol
from organization.models import Organization

class ProtocolForm(forms.ModelForm):

    class Meta:
        model = Protocol
        exclude = ('parent', 'slug', 'duration_in_seconds', 'status','raw', 'author', 'owner', 'published', 'public', 'duration', 'data') # 'data',

    # def __init__(self, *args, **kwargs):
    #     super(ProtocolForm, self).__init__(*args, **kwargs)
    #     choices = [(pt.id, unicode(pt.name)) for pt in Organization.objects.all()]
    #     self.fields['owner'].choices = choices
