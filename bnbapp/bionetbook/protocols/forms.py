#import floppyforms as forms
from django import forms

from protocols.models import Protocol


class ProtocolForm(forms.ModelForm):

    class Meta:
        model = Protocol
        exclude = ('parent', 'owner', 'slug', 'duration_in_seconds', 'status', 'version',)


class PublishForm(forms.Form):
    pass

class StepForm(forms.Form):
    name = forms.CharField(max_length=100)
    remark = forms.CharField()

class ActionForm(forms.Form):

    VERB_CHOICES = (('add','Add'), ('mix','Mix'))

    name = forms.CharField(max_length=100)
    remark = forms.CharField()
    duration = forms.IntegerField()
    #verb = forms.CharField(choice=VERB_CHOICES)
