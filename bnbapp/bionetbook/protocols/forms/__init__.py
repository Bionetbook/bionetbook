import floppyforms as forms

from protocols.forms.baseforms import ProtocolForm


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
