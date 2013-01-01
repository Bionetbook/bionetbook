import floppyforms as forms
from protocols.models import Protocol

class ProtocolForm(forms.ModelForm):

    class Meta:
        model = Protocol
        exclude = ('parent', 'owner', 'slug', 'duration_in_seconds', 'status', 'version',)


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
    pass

forms.VerbForm = VerbForm
