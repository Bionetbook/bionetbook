import floppyforms as forms

#from protocols.forms.baseforms import ProtocolForm

from protocols.models import Protocol
from organization.models import Organization

class ProtocolForm(forms.ModelForm):

    class Meta:
        model = Protocol
        exclude = ('parent', 'slug', 'duration_in_seconds', 'status', 'version','raw')

    def __init__(self, *args, **kwargs):
        super(ProtocolForm, self).__init__(*args, **kwargs)
        choices = [(pt.id, unicode(pt.name)) for pt in Organization.objects.all()]
        self.fields['owner'].choices = choices


class PublishForm(forms.Form):
    pass


class StepForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    remark = forms.CharField(required=False)


class ActionForm(forms.Form):

    name = forms.CharField(max_length=100, required=False)
    remark = forms.CharField(required=False)
    time_units = forms.CharField(required=False)
    duration = forms.IntegerField()
    duration_comment = forms.CharField(required=False)


class VerbForm(forms.Form):
    has_components = False
    has_machines = False

forms.VerbForm = VerbForm


# class ComponentForm(forms.Form):
#     name = forms.CharField(max_length=100, required=False)
#     remark = forms.CharField(required=False)
